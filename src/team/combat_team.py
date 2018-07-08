from typing import List

from src.combat.combat_actions import KnockedOut, ElementalAction, Switch, Action
from src.elemental.ability.ability import Ability
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
        self.attempt_switch(0)  # The first eligible (HP > 0) Elemental in the team

    def end_combat(self) -> None:
        if self.owner and not self.owner.is_npc:
            self.owner.is_busy = False

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

    def select_ability(self, i: int) -> bool:
        """
        Uses one of the active Elemental's abilities.
        TODO Check if the Elemental is incapacitated for the turn.
        :param i: The position of the ability in the active Elemental's abilities list.
        :return bool: True if the request was made. Note that a request is different from resolution.
        """
        is_valid_selection = 0 <= i < len(self.active_elemental.available_abilities)
        if not is_valid_selection:
            return False
        selected_ability = self.active_elemental.abilities[i]
        action = ElementalAction(
            actor=self.active_elemental,
            ability=selected_ability,
            target=self.combat.get_target(selected_ability, self.active_elemental)
        )
        self.combat.request_action(action)
        return True

    def on_turn_start(self) -> None:
        self.active_elemental.start_turn()
        for elemental in self.eligible_bench:
            elemental.gain_bench_mana()

    def attempt_switch(self, slot: int) -> bool:
        """
        Switch the active Elemental with an Elemental on CombatTeam.eligible.
        :return bool: True if the request to switch was made. Note that a request is different from resolution.
        """
        eligible_elementals = self.eligible_bench
        is_valid_slot = 0 <= slot < len(eligible_elementals)
        if not is_valid_slot:
            return False
        switch = Switch(
            team=self,
            old_active=self.active_elemental,
            new_active=eligible_elementals[slot]
        )
        self.combat.request_action(switch)
        return True

    def change_active_elemental(self, elemental: CombatElemental) -> None:
        self.__active_elemental = elemental

    def end_turn(self) -> None:
        self.active_elemental.end_turn()
        # Check knocked out again in case a debuff, etc. finished off the Elemental
        if self.active_elemental.is_knocked_out:
            # TODO
            pass

    def add_action(self, action: Action) -> None:
        # Store the Action as a record.
        self._actions.append(action)