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
        self.logs = [[]]  # List[List[EventLog]]; events are grouped by rounds

    def add_log(self, recap: str) -> None:
        # Ignore events with no recap message.
        if recap:
            log = self._make_log(recap)
            self.logs[-1].append(log)

    @property
    def most_recent_index(self) -> int:
        return self.num_logs - 1

    @property
    def most_recent_log(self) -> EventLog:
        return self.logs[self.most_recent_index][-1]

    @property
    def num_logs(self) -> int:
        """
        The number of logs, except for the most recent one (which is awaiting the current turn's logs to be appended).
        """
        return len(self.logs) - 1

    def get_turn_logs(self, from_index: int) -> List[List[EventLog]]:
        """
        Show logs starting from an index, while truncating the empty entry at the end.
        """
        return self.logs[from_index:self.num_logs]

    def prepare_new_round(self) -> None:
        self.logs.append([])

    def add_ko(self, combat_elemental) -> None:
        self.add_log(f'{combat_elemental.nickname} was knocked out!')

    def append_recent(self, recap: str) -> None:
        """
        For the recaps that don't need to be in its own dialog box, they can be appended to the previous one.
        """
        current_turn_events = self.logs[-1]
        if recap and current_turn_events:
            current_turn_events[-1].append_recap(recap)

    def continue_recent(self, recap: str) -> None:
        """
        Creates a new snapshot, but uses the previous log's message and appends the recap on top of it.
        """
        current_turn_events = self.logs[-1]
        if recap and current_turn_events:
            previous_recap = current_turn_events[-1].recap
            new_recap = '\n'.join([previous_recap, recap])
            self.add_log(new_recap)

    def _make_log(self, recap) -> EventLog:
        # Fall back on empty list if there are no active elementals on a side.
        side_a = []
        for elemental in self.combat.side_a_active:
            side_a.append(elemental.snapshot())
        side_b = []
        for elemental in self.combat.side_b_active:
            side_b.append(elemental.snapshot())
        return EventLog(side_a, side_b, recap)


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
