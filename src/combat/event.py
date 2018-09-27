from typing import List

from src.elemental.combat_elemental import CombatElementalLog


class EventLog:
    """
    Record an event that occurs within an Action, eg. what happened on turn end.
    This is for rendering purposes.
    """

    def __init__(self,
                 side_a: List[CombatElementalLog],
                 side_b: List[CombatElementalLog],
                 recap: str,
                 acting_team):
        """
        :param acting_team: CombatTeam
        """
        self.side_a = side_a
        self.side_b = side_b
        self.recap = recap
        self.acting_team = acting_team

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

    def add_log(self, recap: str, acting_team) -> None:
        # Ignore events with no recap message.
        if recap:
            log = self._make_log(recap, acting_team)
            self.logs[-1].append(log)

    @property
    def most_recent_index(self) -> int:
        """
        :return the most recent log index, excluding the empty [] added when preparing a new round.
        """
        if self.logs[-1]:
            return len(self.logs)
        return len(self.logs) - 1

    @property
    def most_recent_log(self) -> EventLog:
        for log_group in reversed(self.logs):
            if log_group:
                return log_group[-1]

    def get_turn_logs(self, from_index: int) -> List[List[EventLog]]:
        return self.logs[from_index:self.most_recent_index]

    def prepare_new_round(self) -> None:
        self.logs.append([])

    def add_ko(self, combat_elemental) -> None:
        self.add_log(f'{combat_elemental.nickname} was knocked out!', combat_elemental.team)

    def append_recent(self, recap: str) -> None:
        """
        For the recaps that don't need to be in its own dialog box, they can be appended to the previous one.
        """
        current_turn_events = self.logs[-1]
        if recap and current_turn_events:
            current_turn_events[-1].append_recap(recap)

    def continue_recent(self, recap: str, acting_team) -> None:
        """
        Creates a new snapshot, but uses the previous log's message and appends the recap on top of it.
        """
        current_turn_events = self.logs[-1]
        if recap and current_turn_events:
            previous_recap = current_turn_events[-1].recap
            new_recap = '\n'.join([previous_recap, recap])
            self.add_log(new_recap, acting_team)

    def _make_log(self, recap, acting_team) -> EventLog:
        # Fall back on empty list if there are no active elementals on a side.
        side_a = []
        for elemental in self.combat.side_a_active:
            side_a.append(elemental.snapshot())
        side_b = []
        for elemental in self.combat.side_b_active:
            side_b.append(elemental.snapshot())
        return EventLog(side_a, side_b, recap, acting_team)
