from typing import List

from src.character.inventory import ItemSlot
from src.combat.actions.casting import Casting
from src.combat.actions.combat_actions import Switch, Action, UseItem
from src.combat.actions.elemental_action import ElementalAction
from src.core.elements import Elements
from src.core.targetable_interface import Targetable
from src.elemental.ability.ability import Ability
from src.elemental.ability.queueable import Castable
from src.elemental.combat_elemental import CombatElemental
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
                 elementals: List[Elemental],
                 owner=None):
        """
        :param owner: NPC or None
        """
        self.combat = None
        self.__elementals = [CombatElemental(elemental, self) for elemental in elementals]
        self.owner = owner
        self.__active_elemental = None
        self._status_effects = []  # Team-wide status effects, eg. weather.
        self._actions = []  # list[Action] taken by this team.
        self.side = None  # Str. The side of the battlefield this CombatTeam is on.
        self.logger = None  # Later set by Combat.
        self.exp_earned = 0  # Counts how much experience was earned this battle.
        self.gold_earned = 0
        self._items_earned = {}  # {item_name: ItemSlot}

    @staticmethod
    def from_team(team: Team) -> 'CombatTeam':
        """
        Convert a Team containing Elementals to a CombatTeam with CombatElementals.
        """
        return CombatTeam(team.elementals, team.owner)

    def set_combat(self, combat) -> None:
        """
        :param combat: The battle this Team is joining.
        """
        self.combat = combat
        self.logger = combat.turn_logger
        if self.owner and not self.owner.is_npc:
            self.owner.set_combat_team(self)

    def set_side(self, side: str) -> None:
        self.side = side

    def on_combat_start(self) -> None:
        self.attempt_switch(self.eligible_bench[0])  # The first eligible (HP > 0) Elemental in the team

    def end_combat(self) -> None:
        if self.owner and not self.owner.is_npc:
            self.owner.clear_combat()

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
        if not self.active_elemental:
            return len(self.eligible_bench) > 0
        return self.active_elemental.can_switch and len(self.eligible_bench) > 0

    @property
    def eligible_bench(self) -> List[CombatElemental]:
        """
        Returns the benched CombatElementals that aren't knocked out (ie. have more than 0 HP).
        """
        return [elemental for elemental in self.__elementals
                if elemental != self.__active_elemental and not elemental.is_knocked_out]

    @property
    def status_effects(self) -> List[StatusEffect]:
        """
        :return: A list of team-targeting status effects (as opposed to forwarding the active elemental's).
        """
        return list(self._status_effects)

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
    def get_knocked_out(self) -> List[CombatElemental]:
        """
        All the knocked out elementals on this team, for rendering purposes.
        """
        return [elemental for elemental in self.__elementals if elemental.is_knocked_out]

    @property
    def last_action(self) -> Action:
        previous = len(self._actions) - 1
        return self._actions[previous]

    @property
    def available_abilities(self) -> List[Ability]:
        return self.active_elemental.available_abilities.copy()

    @property
    def items_earned(self):
        return self._items_earned.values()

    def add_items(self, items) -> None:
        """
        :param items: List[Item]
        self.items_earned is a dict {item_name: ItemSlot}, similar to Inventory.
        """
        if self.owner is None:
            return
        for item in items:
            if item.name in self._items_earned:
                self._items_earned[item.name].update_amount(1)
            else:
                self._items_earned[item.name] = ItemSlot(item, 1)
            self.owner.add_item(item)

    def add_gold(self, amount: int) -> None:
        self.gold_earned += amount
        if self.owner:
            self.owner.update_gold(amount)

    def add_exp(self, amount: int) -> None:
        self.exp_earned += amount
        if self.owner:
            self.owner.add_exp(amount)
        for elemental in self.elementals:
            if not elemental.is_knocked_out:
                elemental.add_exp(amount)

    def check_casting(self) -> bool:
        """
        Is our currently active elemental locked into an ability?
        If true, automatically continue that ability.
        """
        action_queued = self.active_elemental.action_queued
        if not action_queued:
            return False
        if action_queued.is_ready:
            self.make_move(action_queued.ability)
        else:
            # Handle a continued cast time. Only a Castable should ever reach this block.
            self.handle_cast_time(action_queued)
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
            castable=castable
        )
        self.combat.request_action(action)

    def make_move(self, ability) -> None:
        action = ElementalAction(
            actor=self.active_elemental,
            ability=ability,
            combat=self.combat
        )
        self.combat.request_action(action)

    def turn_start(self) -> None:
        self.active_elemental.start_turn()
        for effect in self._status_effects:
            if effect.on_turn_start():
                self.log(effect.trigger_recap)
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

    def use_item(self, item, elemental: CombatElemental):
        self.combat.request_action(UseItem(
            item,
            elemental,
            combat_team=self
        ))

    def change_active_elemental(self, elemental: CombatElemental) -> None:
        # Logging is handled in Switch action as it has a detailed recap.
        self.__active_elemental = elemental

    def end_turn(self) -> None:
        """
        When this elemental's move has been resolved.
        """
        for effect in self._status_effects:
            if effect.on_turn_end():
                self.log(effect.trigger_recap)
            effect.reduce_turn_duration()
            if effect.duration_ended:
                self._status_effects.remove(effect)
        self.active_elemental.end_turn()

    def end_round(self) -> None:
        """
        When everybody's moves have been resolved.
        """
        for effect in self._status_effects:
            if effect.on_round_end():
                self.log(effect.trigger_recap)
            effect.reduce_round_duration()
            if effect.duration_ended:
                self._status_effects.remove(effect)
        self.active_elemental.end_round()

    def add_action(self, action: Action) -> None:
        # Store the Action as a record.
        self._actions.append(action)

    def add_status_effect(self, effect: StatusEffect) -> None:
        equivalent_effect = self.__effect_exists(effect)
        if equivalent_effect and not effect.can_add_instances:
            equivalent_effect.reapply()
            return
        effect.target = self
        if effect.applier == self.active_elemental:
            effect.boost_turn_duration()
        self._status_effects.append(effect)
        effect.on_effect_start()
        self.append_recent_log(effect.application_recap)

    # Targetable implementations: Reroute attacks, etc. to the currently active elemental.

    def heal(self, amount: int) -> None:
        # Trying to heal a CombatTeam to do damage just goes to the active elemental.
        self.active_elemental.heal(amount)

    def receive_damage(self, amount: int, actor: CombatElemental) -> None:
        # Trying to target a CombatTeam to do damage just goes to the active elemental.
        self.active_elemental.receive_damage(amount, actor)

    def on_receive_ability(self, ability: Ability, actor: CombatElemental) -> None:
        # Same as receive damage.
        self.active_elemental.on_receive_ability(ability, actor)

    def update_mana(self, amount: int) -> None:
        self.active_elemental.update_mana(amount)

    def log(self, recap) -> None:
        self.logger.add_log(recap, acting_team=self)

    def append_recent_log(self, recap: str) -> None:
        self.logger.append_recent(recap)

    def continue_recent_log(self, recap: str) -> None:
        self.logger.continue_recent(recap, acting_team=self)

    @property
    def nickname(self) -> str:
        return self.active_elemental.nickname

    @property
    def is_knocked_out(self) -> bool:
        return self.active_elemental.is_knocked_out

    @property
    def physical_def(self) -> int:
        return self.active_elemental.physical_def

    @property
    def element(self) -> Elements:
        return self.active_elemental.element

    @property
    def damage_reduction(self) -> float:
        return self.active_elemental.damage_reduction

    @property
    def magic_def(self) -> int:
        return self.active_elemental.magic_def

    def __effect_exists(self, to_check: StatusEffect) -> StatusEffect or None:
        """
        Check if an equivalent StatusEffect is already on this CombatTeam, by type.
        :return The StatusEffect if it exists, None if not.
        """
        return next((effect for effect in self._status_effects if type(effect) is type(to_check)), None)
