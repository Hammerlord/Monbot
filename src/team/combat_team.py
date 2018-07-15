from typing import List

from src.combat.combat_actions import KnockedOut, ElementalAction, Switch, Action
from src.elemental.ability.ability import Ability, Target
from src.elemental.combat_elemental import CombatElemental
from src.elemental.elemental import Elemental
from src.team.team import Team


class CombatTeam:

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
        self.status_effects = []  # Team-wide status effects, eg. weather.
        self._actions = []  # list[Action] taken by this team.
        self._enemy_side = None  # List[CombatTeam] All the teams opposing this one.

    @property
    def enemy_side(self) -> List['CombatTeam']:
        return self._enemy_side.copy()

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

    def on_combat_start(self) -> None:
        self.attempt_switch(self.eligible_bench[0])  # The first eligible (HP > 0) Elemental in the team

    def end_combat(self) -> None:
        if self.owner and not self.owner.is_npc:
            self.owner.is_busy = False

    def set_enemy_side(self, enemy_teams: List['CombatTeam']) -> None:
        self._enemy_side = enemy_teams

    def get_target(self, ability: Ability) -> CombatElemental:
        """
        :return: The CombatElemental the Ability should affect, based on the Ability's targeting enum.
        """
        target = ability.targeting
        if target == Target.SELF:
            return self.active_elemental
        elif target == Target.ENEMY:
            return self.get_active_enemy()

    @property
    def last_action(self) -> Action:
        return self._actions[-1]

    def get_active_enemy(self) -> CombatElemental:
        """
        :return: The first CombatElemental on the opposing side.
        TODO work in progress: this, of course, doesn't support multiple elementals on one side.
        """
        return self._enemy_side[0].active_elemental

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

    def select_ability(self, ability: Ability) -> bool:
        """
        Uses one of the active Elemental's abilities.
        TODO Check if the Elemental is incapacitated for the turn.
        :param ability: The Ability to use.
        :return bool: True if the request was made. Note that a request is different from resolution.
        """
        if ability not in self.active_elemental.available_abilities:
            return False
        action = ElementalAction(
            actor=self.active_elemental,
            ability=ability,
            target=self.get_target(ability)
        )
        self.combat.request_action(action)
        return True

    def on_turn_start(self) -> None:
        self.active_elemental.start_turn()
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
        self.active_elemental.end_turn()

    def end_round(self) -> None:
        """
        When everybody's moves have been resolved.
        """
        self.active_elemental.end_round()

    def add_log(self, action: Action) -> None:
        # Store the Action as a record.
        self._actions.append(action)
