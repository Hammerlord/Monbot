from typing import List

from src.combat.combat_actions import KnockedOut, ElementalAction, Switch, Action
from src.elemental.ability.ability import Ability
from src.elemental.combat_elemental import CombatElemental
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
        self.owner = team.owner
        self.__active_elemental = None
        self.status_effects = []  # Team-wide status effects, eg. weather.
        self._actions = []  # list[Action] taken by this team.
        self.switch(0)  # The first eligible (HP > 0) Elemental in the team

    def set_combat(self, combat) -> None:
        """
        :param combat: The battle this Team is joining.
        """
        self.combat = combat
        self.combat.join_battle(self)
        self.owner.is_busy = True

    def end_combat(self) -> None:
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
        return self.owner.is_npc

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
        return self.active_elemental.available_abilities

    def select_ability(self, i: int) -> bool:
        """
        Uses one of the active Elemental's abilities.
        TODO Check if the Elemental is incapacitated for the turn.
        :param i: The position of the ability in the active Elemental's abilities list.
        :return bool: True if a recordable Action was made.
        """
        is_valid_selection = 0 <= i < len(self.active_elemental.available_abilities)
        if not is_valid_selection:
            return False
        selected_ability = self.active_elemental.abilities[i]
        self.__use_ability(selected_ability)
        return True

    def on_turn_start(self) -> None:
        self.active_elemental.start_turn()
        for elemental in self.eligible_bench:
            elemental.gain_bench_mana()

    def switch(self, slot: int) -> bool:
        """
        Switch the active Elemental with an Elemental on CombatTeam.eligible.
        :return bool: True if a switch succeeded.
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
        self.__execute_action(switch)
        return True

    def change_active_elemental(self, elemental: CombatElemental):
        self.__active_elemental = elemental

    def end_turn(self) -> None:
        self.active_elemental.end_turn()
        # Check knocked out again in case a debuff, etc. finished off the Elemental
        if self.active_elemental.is_knocked_out:
            self.__handle_knockout()

    def __use_ability(self, ability: Ability) -> None:
        if self.active_elemental.is_knocked_out:
            self.__handle_knockout()
        else:
            self.__make_action(ability)
            self.end_turn()
        self.combat.check_end()

    def __handle_knockout(self) -> None:
        action = KnockedOut(self.active_elemental)
        self.__execute_action(action)

    def __execute_action(self, action: Action) -> None:
        action.execute()
        # Store the Action as a record.
        self._actions.append(action)

    def __make_action(self, ability: Ability) -> None:
        """
        Execute the Ability and create a log for it.
        """
        action = ElementalAction(
            actor=self.active_elemental,
            ability=ability,
            target=self.combat.get_target(ability, self.active_elemental)
        )
        self.__execute_action(action)
        self.__active_elemental.add_action(action)