from itertools import groupby
from random import random
from typing import List

from src.combat.actions.action import EventLogger, EventLog
from src.combat.actions.combat_actions import Action, Switch
from src.combat.combat_ai import CombatAI
from src.core.targetable_interface import Targetable
from src.elemental.ability.ability import Ability, Target
from src.elemental.combat_elemental import CombatElemental


class Combat:
    """
    How CombatTeams communicate.
    Two opposing sides to a battlefield are distinguished, internally, by "side_a" and "side_b".
    TODO for now we only have 1v1, even though each side allows multiple CombatTeams to join.
    """
    SIDE_A = 'a'  # Note: 'a' and 'b' are arbitrary.
    SIDE_B = 'b'

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
        self.turn_logger = EventLogger(self)
        self.num_rounds = 0
        self.winning_side = None  # List[CombatTeam] The teams who won.
        self.losing_side = None

    @property
    def teams(self):
        """
        :return: List[CombatTeam] - All CombatTeams currently participating in this battle.
        """
        return self.side_a + self.side_b  # Defensive

    @property
    def side_a_active(self) -> List[CombatElemental]:
        return [team.active_elemental for team in self.side_a if team.active_elemental]

    @property
    def side_b_active(self) -> List[CombatElemental]:
        return [team.active_elemental for team in self.side_b if team.active_elemental]

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

    @property
    def is_waiting_for_players(self) -> bool:
        return len(self.teams) < 2 and not self.in_progress

    def check_combat_start(self) -> None:
        if len(self.teams) >= 2 and not self.in_progress:  # TODO 1v1 only right now
            self.in_progress = True
            for team in self.side_a:
                team.set_side(Combat.SIDE_A)
                team.on_combat_start()
            for team in self.side_b:
                team.set_side(Combat.SIDE_B)
                team.on_combat_start()

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
            self._add_knockout_replacement(request)
            if len(self.action_requests) == len(self.get_knockouts()):
                self._resolve_requests()
        else:
            self.action_requests.append(request)
            if len(self.action_requests) == len(self.teams):
                self._resolve_requests()

    def get_target(self, ability: Ability, actor: CombatElemental) -> Targetable:
        """
        :return: The Targetable the Ability should affect, based on the Ability's targeting enum.
        """
        target = ability.targeting
        if target == Target.SELF:
            return actor
        if target == Target.SELF_TEAM:
            return actor.team
        elif target == Target.ENEMY:
            return self.get_active_enemy(actor.team)
        elif target == Target.ENEMY_CLEAVE:
            # TODO
            return self.get_active_enemy(actor.team)
        elif target == Target.ENEMY_AOE:
            # TODO
            return self.get_active_enemy(actor.team)
        elif target == Target.ENEMY_TEAM:
            return self.get_enemy_side(actor.team)[0]
        raise ValueError(f"{ability.name} has no valid targeting.")

    def get_enemy_side(self, team):
        """
        :param team: CombatTeam. The Team that is looking for an enemy.
        :return: List[CombatTeam]
        """
        assert team.side is not None
        if team.side == Combat.SIDE_A:
            return list(self.side_b)
        if team.side == Combat.SIDE_B:
            return list(self.side_a)

    def get_active_enemy(self, team):
        """
        :param team: CombatTeam. The Team that is looking for an enemy.
        :return: CombatElemental
        """
        return self.get_enemy_side(team)[0].active_elemental

    def _add_knockout_replacement(self, request: Action) -> None:
        if isinstance(request, Switch) and request.team in self.get_knockouts():
            self.action_requests.append(request)

    def _resolve_requests(self) -> None:
        """
        When all players have made an action request, resolve the order and execution of those requests.
        """
        kos = []  # List[CombatElemental]: elementals knocked out this turn
        for action_group in self._get_priority_order_requests():
            # If multiple Actions share the same TurnPriority,
            # next determine order by the speed of the elemental. TODO same speed should roll.
            action_group = sorted(action_group, key=lambda action: action.speed, reverse=True)
            for action in action_group:
                self._resolve_request(action)
                self._check_kos(kos)
                if self.check_combat_end():
                    self.prepare_new_round()  # Currently, logging needs the empty []
                    return
        self._end_round()

    def _end_round(self):
        self.num_rounds += 1
        for team in self.teams:
            team.end_round()
        self.prepare_new_round()

    def _check_kos(self, already_checked: List[CombatElemental]) -> None:
        """
        If an elemental has been knocked out after a request (on either side), record the log and grant exp.
        """
        for team in self.teams:
            elemental = team.active_elemental
            if elemental and elemental.is_knocked_out and elemental not in already_checked:
                self.turn_logger.add_ko(elemental)
                self._grant_exp(elemental)
                already_checked.append(elemental)

    def _grant_exp(self, from_elemental: CombatElemental) -> None:
        # Grant the opposition experience.
        if not self.allow_exp_gain:
            return
        enemy_side = self.get_enemy_side(from_elemental.team)
        raw_exp = from_elemental.level * 6 + 10
        exp_gained = int(raw_exp // len(enemy_side) + raw_exp * len(enemy_side) * 0.25)
        for enemy_team in enemy_side:
            if not enemy_team.is_npc:
                enemy_team.add_exp(exp_gained)

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
        self.turn_logger.prepare_new_round()
        print([log for log in self.turn_logger.logs[-2]])
        if not self.in_progress:
            return
        for team in self.teams:
            if not self.is_awaiting_knockout_replacements():
                # Do not regen mana while we wait for new Elementals to be sent in.
                team.turn_start()
            if team.check_casting():
                continue
            if team.is_npc:
                # Automatically make a move for NPC teams.
                CombatAI(team, self).pick_move()

    @property
    def previous_round_actions(self) -> List[Action]:
        """
        Get all the Actions from the previous round of turns.
        prepare_new_round() always creates an empty new log [] by the time this is called,
        so we want to retrieve the second last log.
        """
        return self.action_log[-2]

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

    def check_combat_end(self) -> bool:
        did_side_a_lose = all([team.is_all_knocked_out for team in self.side_a])
        did_side_b_lose = all([team.is_all_knocked_out for team in self.side_b])
        if did_side_a_lose and did_side_b_lose:
            pass  # Tie
        elif did_side_a_lose:
            self.winning_side = self.side_b
            self.losing_side = self.side_a
        elif did_side_b_lose:
            self.winning_side = self.side_a
            self.losing_side = self.side_b
        if did_side_a_lose or did_side_b_lose:
            self.end_combat()
            return True

    def end_combat(self) -> None:
        self.in_progress = False
        self._grant_loot()
        for team in self.teams:
            team.end_combat()
        print(f"Completed battle in {self.num_rounds} rounds.")

    def _grant_loot(self) -> None:
        if self.losing_side is None:
            return
        gold_earned = self._calculate_gold_earned()
        items_dropped = self._roll_items_dropped()
        for team in self.winning_side:
            team.add_gold(gold_earned)
            team.add_items(items_dropped)

    def _roll_items_dropped(self):
        """
        Only wild Elementals drop loot.
        :return: List[Item]
        """
        items = []
        for team in self.losing_side:
            if team.owner is not None:
                continue
            for loot in team.loot:
                if random() <= loot.drop_rate:
                    items.append(loot.item)
        return items

    def _calculate_gold_earned(self) -> int:
        """
        Calculate gold based on the losing side, if their teams have an owner (and therefore money).
        Note this doesn't actually deduct any gold.
        """
        gold = 0
        for team in self.losing_side:
            if team.owner:
                gold += team.owner.level
        return gold

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
