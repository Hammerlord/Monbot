from typing import List

from src.combat.actions.casting import Casting
from src.combat.actions.combat_actions import Switch, Action
from src.combat.actions.elemental_action import ElementalAction
from src.core.targetable_interface import Targetable
from src.elemental.ability.ability import Ability, Target, Castable
from src.elemental.combat_elemental import CombatElemental, CombatElementalLog
from src.elemental.elemental import Elemental
from src.elemental.status_effect.status_effect import StatusEffect
from src.team.team import Team


class CombatTeam(Targetable):
    """
    Wrapper class for a Team in battle. Generates CombatElemental instances of the Team's Elementals.
    The player controls the CombatTeam.
    TODO entering combat should fail if all Elementals have been knocked out.
    """

    def __init__(self,
                 team: Team):
        """
        :param team: The non-combat Team.
        """
        self.combat = None
        self.__elementals = [CombatElemental(elemental, self) for elemental in team.elementals]
        self.owner = team.owner  # Character or None
        self.__active_elemental = None
        self._status_effects = []  # Team-wide status effects, eg. weather.
        self._actions = []  # list[Action] taken by this team.
        self.side = None  # Str. The side of the battlefield this CombatTeam is on.

    @staticmethod
    def from_elementals(elementals: List[Elemental]) -> 'CombatTeam':
        """
        Wild Elementals don't have a formal team, so this function makes a dummy one for them.
        """
        team = Team(owner=None)
        for elemental in elementals:
            team.add_elemental(elemental)
        return CombatTeam(team)

    def set_combat(self, combat) -> None:
        """
        :param combat: The battle this Team is joining.
        """
        self.combat = combat
        self.combat.join_battle(self)
        if self.owner and not self.owner.is_npc:
            self.owner.is_busy = True

    def set_side(self, side: str) -> None:
        self.side = side

    def on_combat_start(self) -> None:
        self.attempt_switch(self.eligible_bench[0])  # The first eligible (HP > 0) Elemental in the team

    def end_combat(self) -> None:
        if self.owner and not self.owner.is_npc:
            self.owner.is_busy = False

    @property
    def last_action(self) -> Action:
        return self._actions[-1]

    @property
    def elementals(self) -> List[CombatElemental]:
        """
        :return: All CombatElementals on this team, including the active one.
        """
        return self.__elementals.copy()

    @property
    def active_elemental(self) -> CombatElemental:
        return self.__active_elemental

    @property
    def bench(self) -> List[CombatElemental]:
        """
        Returns the team CombatElementals minus the active one.
        """
        return [elemental for elemental in self.__elementals if elemental != self.__active_elemental]

    @property
    def can_switch(self) -> bool:
        return len(self.eligible_bench) > 0

    @property
    def eligible_bench(self) -> List[CombatElemental]:
        """
        Returns the benched CombatElementals that aren't knocked out (ie. have more than 0 HP).
        """
        return [elemental for elemental in self.__elementals
                if elemental != self.__active_elemental and not elemental.is_knocked_out]

    @property
    def is_npc(self) -> bool:
        """
        Should this CombatTeam auto-battle?
        True if: No owner (wild elementals), or owner is an NPC.
        """
        return not self.owner or self.owner.is_npc

    @property
    def is_all_knocked_out(self) -> bool:
        """
        :return bool: If all Elementals on the Team have been knocked out (0 HP).
        Game over if true.
        """
        return all(elemental.is_knocked_out for elemental in self.__elementals)

    @property
    def last_action(self) -> Action:
        previous = len(self._actions) - 1
        return self._actions[previous]

    @property
    def available_abilities(self) -> List[Ability]:
        return self.active_elemental.available_abilities.copy()

    def check_casting(self) -> bool:
        """
        Is our currently active elemental locked into casting an ability?
        If true, automatically continue that ability.
        """
        castable = self.active_elemental.casting
        if not castable:
            return False
        if castable.is_ready:
            self.make_move(castable.ability)
        else:
            self.handle_cast_time(castable)
        return True

    def select_ability(self, ability: Ability) -> bool:
        """
        Uses one of the active Elemental's abilities.
        TODO Check if the Elemental is incapacitated for the turn.
        :param ability: The Ability to use.
        :return bool: True if the request was made. Note that a request is different from resolution.
        """
        if not ability.is_usable_by(self.active_elemental):
            return False
        if ability.has_cast_time:
            self.handle_cast_time(Castable(ability))
        else:
            self.make_move(ability)
        return True

    def handle_cast_time(self, castable: Castable) -> None:
        action = Casting(
            actor=self.active_elemental,
            castable=castable,
            target=self.combat.get_target(castable.ability, self.active_elemental)  # This might not be the end target.
        )
        self.combat.request_action(action)

    def make_move(self, ability) -> None:
        self.active_elemental.casting = None
        action = ElementalAction(
            actor=self.active_elemental,
            ability=ability,
            target=self.combat.get_target(ability, self.active_elemental)
        )
        self.combat.request_action(action)

    def turn_start(self) -> None:
        self.active_elemental.start_turn()
        for effect in self._status_effects:
            effect.on_turn_start()
        for elemental in self.eligible_bench:
            elemental.gain_bench_mana()

    def attempt_switch(self, elemental: CombatElemental) -> bool:
        """
        Switch the active Elemental with an Elemental on CombatTeam.eligible.
        :return bool: True if the request to switch was made. Note that a request is different from resolution.
        """
        if elemental not in self.eligible_bench:
            return False
        switch = Switch(
            team=self,
            old_active=self.active_elemental,
            new_active=elemental
        )
        self.combat.request_action(switch)
        return True

    def change_active_elemental(self, elemental: CombatElemental) -> None:
        self.__active_elemental = elemental

    def end_turn(self) -> None:
        """
        When this elemental's move has been resolved.
        """
        for effect in self._status_effects:
            effect.on_turn_end()
        self.active_elemental.end_turn()

    def end_round(self) -> None:
        """
        When everybody's moves have been resolved.
        """
        for effect in self._status_effects:
            effect.reduce_duration()
            if effect.duration_ended:
                self._status_effects.remove(effect)
        self.active_elemental.end_round()

    def add_log(self, action: Action) -> None:
        # Store the Action as a record.
        self._actions.append(action)

    def add_status_effect(self, status_effect: StatusEffect) -> None:
        status_effect.target = self
        self._status_effects.append(status_effect)
        status_effect.on_effect_start()

    def heal(self, amount: int) -> None:
        """
        When CombatTeam receives a heal, all eligible elementals receives that amount of healing.
        """
        self.active_elemental.heal(amount)
        for elemental in self.eligible_bench:
            elemental.heal(amount)

    def receive_damage(self, amount: int, actor: CombatElemental) -> None:
        # However, trying to target a CombatTeam to do damage just goes to the active elemental.
        self.active_elemental.receive_damage(amount, actor)

    def on_receive_ability(self, ability: Ability, actor: CombatElemental) -> None:
        # Same as receive damage.
        self.active_elemental.on_receive_ability(ability, actor)

    def snapshot(self) -> CombatElementalLog:
        return self.active_elemental.snapshot()
