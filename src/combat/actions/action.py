from enum import Enum
from typing import List

from src.core.targetable_interface import Targetable
from src.elemental.ability.ability import TurnPriority
from src.elemental.combat_elemental import CombatElementalLog


class ActionType(Enum):
    NONE = 0
    ELEMENTAL_ACTION = 1
    SWITCH = 2
    ITEM = 3


class EventLog:
    """
    Record an event that occurs within an Action, eg. what happened on turn end.
    This is for rendering purposes.
    """

    def __init__(self,
                 side_a: List[CombatElementalLog],
                 side_b: List[CombatElementalLog],
                 recap: str):
        self.side_a = side_a
        self.side_b = side_b
        self.recap = recap

    def __repr__(self) -> str:
        return self.recap

    def append_recap(self, new_recap: str) -> None:
        self.recap = f'{self.recap}\n{new_recap}'


class EventLogger:
    """
    Takes a snapshot of every currently-active elemental when asked to make a log.
    The snapshots are static representations of the elemental's state, which is otherwise mutable.
    """

    def __init__(self, combat):
        """
        :param combat: Combat
        """
        self.combat = combat
        self.events = [[]]  # List[List[EventLog]]; events are grouped by rounds

    def add_log(self, recap: str) -> None:
        # Ignore events with no recap message.
        if recap:
            # Fall back on empty list if there are no active elementals on a side.
            side_a = []
            for elemental in self.combat.side_a_active:
                side_a.append(elemental.snapshot())
            side_b = []
            for elemental in self.combat.side_b_active:
                side_b.append(elemental.snapshot())
            log = EventLog(side_a, side_b, recap)
            self.events[-1].append(log)

    def get_previous_turn_logs(self) -> List[EventLog]:
        return list(self.events[-2])

    def prepare_new_round(self) -> None:
        self.events.append([])

    def add_ko(self, combat_elemental) -> None:
        self.add_log(f'{combat_elemental.nickname} was knocked out!')

    def append_recent(self, recap: str) -> None:
        """
        For the recaps that don't need to be in its own dialog box, they can be appended to the previous one.
        """
        if recap:
            self.events[-1][-1].append_recap(recap)


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
