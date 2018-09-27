from enum import Enum
from typing import List

from src.elemental.ability.ability import TurnPriority


class ActionType(Enum):
    NONE = 0
    ELEMENTAL_ACTION = 1
    SWITCH = 2
    ITEM = 3


class Action:
    """
    Base action class. Actions capture a move made by a combatant.
    """

    def __repr__(self):
        return self.recap

    @property
    def action_type(self) -> ActionType:
        raise NotImplementedError

    @property
    def turn_priority(self) -> TurnPriority:
        raise NotImplementedError

    @property
    def team(self):
        """
        :return: CombatTeam: To identify the "owner" of this action.
        """
        raise NotImplementedError

    @property
    def speed(self) -> int:
        raise NotImplementedError

    def execute(self) -> None:
        """
        :return: bool: True if the action was successfully executed.
        """
        raise NotImplementedError

    @property
    def recap(self) -> str:
        """
        :return: Summarize the main part of the action.
        """
        raise NotImplementedError

    @property
    def can_execute(self) -> bool:
        raise NotImplementedError

    @property
    def final_damage(self) -> int:
        return 0

    @property
    def damage_blocked(self) -> int:
        return 0


class ActionLogger:
    """
    A collection of Actions taken across a match.
    """

    def __init__(self):
        self.logs = [[]]  # List[List[Action]]

    def add_log(self, action: Action) -> None:
        # Add Action to the most recent round of turns:
        self.logs[-1].append(action)

    def prepare_new_round(self) -> None:
        self.logs.append([])

    @property
    def previous_round_actions(self) -> List[Action]:
        """
        Get all the Actions from the previous round of turns.
        prepare_new_round() adds an empty list, so we want to get the most recent non-empty one.
        """
        for action_group in reversed(self.logs):
            if len(action_group) > 0:
                return action_group
