from itertools import groupby
from typing import List

from src.combat.combat_actions import ActionType, Action, KnockedOut, Switch
from src.combat.combat_ai import CombatAI
from src.elemental.ability.ability import Target, Ability
from src.elemental.combat_elemental import CombatElemental


class Combat:
    """
    How CombatTeams communicate.
    Two opposing sides to a battlefield are distinguished, internally, by "side_a" and "side_b".
    TODO for now we only have 1v1, even though each side allows multiple CombatTeams to join.
    """
    def __init__(self,
                 allow_items=True,
                 allow_flee=True,
                 allow_exp_gain=True):
        self.side_a = []  # List[CombatTeam] One side of the battlefield.
        self.side_b = []  # List[CombatTeam] Another side of the battlefield.
        self.max_teams_per_side = 3
        self.in_progress = False
        self.allow_items = allow_items
        self.allow_flee = allow_flee
        self.allow_exp_gain = allow_exp_gain
        self.action_requests = []  # List[ActionRequest]
        self.action_log = [[]]  # List[List[Action]]  Actions made this battle, in order, grouped by turn rounds.

    @property
    def teams(self):
        """
        :return: List[CombatTeam] - All CombatTeams currently participating in this battle.
        """
        return self.side_a + self.side_b  # Defensive

    def join_battle(self, combat_team) -> bool:
        """
        :param combat_team: CombatTeam
        :return bool: True if we were able to join the battle.
        """
        if not self.__can_join_battle(combat_team):
            return False
        # Automatically join the side that has fewer teams, or side_a if both are equal.
        side_to_join = self.side_a if len(self.side_a) <= len(self.side_b) else self.side_b
        side_to_join.append(combat_team)
        combat_team.set_combat(self)
        self.check_combat_start()
        return True

    def check_combat_start(self) -> None:
        if len(self.teams) >= 2 and not self.in_progress:  # TODO 1v1 only right now
            self.in_progress = True
            for team in self.side_a:
                team.set_enemy_side(self.side_b.copy())
                team.on_combat_start()
            for team in self.side_b:
                team.set_enemy_side(self.side_a.copy())
                team.on_combat_start()

    def add_knockout_replacement(self, request: Action) -> None:
        if not isinstance(request, Switch) or request.team not in self.get_knockouts():
            return
        self.action_requests.append(request)
        if len(self.action_requests) == len(self.get_knockouts()):
            self.resolve_requests()

    def is_awaiting_knockout_replacements(self) -> bool:
        """
        When an elemental has been knocked out, their teams receive a grace turn where
        a new elemental can be sent out without the opponent making an attack against it.
        """
        return len(self.get_knockouts()) > 0

    def request_action(self, request: Action) -> None:
        """
        :param request: An Action requested by a CombatTeam/player.
        It may be different from what gets executed and reported,
        eg., if the elemental gets knocked out before it can make a move.
        """
        if self.is_awaiting_knockout_replacements():
            self.add_knockout_replacement(request)
        self.action_requests.append(request)
        if len(self.action_requests) == len(self.teams):
            self.resolve_requests()

    def resolve_requests(self) -> None:
        """
        When all players have made an action request, resolve the order and execution of those requests.
        """
        kos = []  # List[CombatElemental]: elementals knocked out this turn
        for action_group in self._get_priority_order_requests():
            # If multiple Actions share the same TurnPriority,
            # next determine order by the speed of the elemental.
            action_group = sorted(action_group, key=lambda action: action.speed, reverse=True)
            for action in action_group:
                self._resolve_request(action)
                self.check_kos(kos)
                self.check_combat_end()
        self.end_round()
        self.prepare_new_round()

    def end_round(self):
        for team in self.teams:
            team.active_elemental.end_round()

    def check_kos(self, already_checked: List[CombatElemental]) -> None:
        """
        If an elemental has been knocked out after a request (on either side), record the log and grant exp.
        """
        for team in self.teams:
            elemental = team.active_elemental
            if elemental and elemental.is_knocked_out and elemental not in already_checked:
                ko = KnockedOut(elemental, self)
                self._add_log(ko)
                team.add_log(ko)
                self.grant_exp(elemental)
                already_checked.append(elemental)

    def grant_exp(self, from_elemental: CombatElemental) -> None:
        # Grant the opposition experience.
        if not self.allow_exp_gain:
            return
        enemy_side = from_elemental.team.enemy_side
        raw_exp = from_elemental.level * 6 + 5
        exp_gained = int(raw_exp // len(enemy_side) + raw_exp * len(enemy_side) * 0.25)
        for enemy_team in enemy_side:
            if enemy_team.is_npc:
                continue
            enemy_team.owner.add_exp(exp_gained)
            for elemental in enemy_team.elementals:
                elemental.add_exp(exp_gained)

    def _resolve_request(self, action: Action) -> None:
        if action.can_execute:
            action.execute()
            self._add_log(action)

    def _add_log(self, action: Action) -> None:
        # Add Action to the most recent round of turns:
        self.action_log[-1].append(action)

    def prepare_new_round(self) -> None:
        """
        Add an empty list where the next turn's Actions will be logged. We always add one as the logger looks
        at the second last entry.
        Then, reset action_requests for the next round of moves.
        """
        self.action_log.append([])
        self.action_requests = []
        print([log.__str__() for log in self.previous_round_log], self.in_progress)
        if not self.in_progress:
            return
        for team in self.teams:
            team.on_turn_start()
            if team.is_npc:
                # Automatically make a move for NPC teams.
                CombatAI(team, self).pick_move()

    @property
    def previous_round_log(self) -> List[Action]:
        # Get all the Actions from the previous round of turns.
        # prepare_new_round() always creates an empty new log [] by the time this is called,
        # so we want to retrieve the second last log.
        return self.action_log[-2].copy()

    def _get_priority_order_requests(self) -> List[List[Action]]:
        """
        Group Actions by TurnPriority, in order of fastest Actions to the slowest.
        """
        action_groups = []
        self.action_requests = sorted(self.action_requests, key=lambda action_request: action_request.turn_priority)
        for key, group in groupby(self.action_requests,
                                  lambda action_request: action_request.turn_priority):
            action_groups.append(list(group))
        return action_groups

    def check_combat_end(self) -> None:
        if (all([team.is_all_knocked_out for team in self.side_a]) or
                all([team.is_all_knocked_out for team in self.side_b])):
            self.end_combat()

    def end_combat(self) -> None:
        self.in_progress = False
        for team in self.teams:
            team.end_combat()

    def get_knockouts(self):
        """
        :return: List[CombatTeam] Return teams whose active Elemental was knocked out last turn.
        We then wait for them to send out a new one.
        """
        return [team for team in self.teams if team.active_elemental and team.active_elemental.is_knocked_out]

    def __can_join_battle(self, combat_team) -> bool:
        """
        :param combat_team: CombatTeam trying to join.
        :return: False if:
        1) Neither side has space
        2) The CombatTeam is already in the battle
        3) The battle has already started.
        """
        return (len(self.teams) < self.max_teams_per_side * 2 and
                combat_team not in self.teams and
                not self.in_progress)
