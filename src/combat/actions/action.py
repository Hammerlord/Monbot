from enum import Enum
from typing import List

from src.core.targetable_interface import Targetable
from src.elemental.ability.ability import TurnPriority
from src.elemental.combat_elemental import CombatElementalLog


class ActionType(Enum):
    NONE = 0
    ELEMENTAL_ACTION = 1
    SWITCH = 2
    KNOCKED_OUT = 3
    ITEM = 4


class EventLog:
    """
    Record an event that occurs within an Action, eg. what happened on turn end.
    This is for rendering purposes.
    """
    def __init__(self,
                 target: Targetable,
                 recap: str):
        self.target_snapshot = target.snapshot()
        self.recap = recap

    def __repr__(self) -> str:
        return self.recap


class TurnLogger:
    def __init__(self):
        self.turns = [[]]  # List[List[EventLog]]

    def add_log(self, combat_elemental, recap) -> None:
        # Ignore events with no recap message.
        if recap != '':
            log = EventLog(combat_elemental, recap)
            self.turns[-1].append(log)

    def get_previous_turn_logs(self) -> List[EventLog]:
        return list(self.turns[-2])

    def prepare_new_round(self) -> None:
        self.turns.append([])

    def add_ko(self, combat_elemental) -> None:
        log = EventLog(combat_elemental, f'{combat_elemental.nickname} was knocked out!')
        self.turns[-1].append(log)


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
