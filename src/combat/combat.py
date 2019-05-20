from itertools import groupby
from typing import List

from src.character.character import Character
from src.combat.actions.action import ActionLogger
from src.combat.actions.combat_actions import Action, Switch
from src.combat.combat_ai import CombatAI
from src.combat.event import EventLogger
from src.combat.loot_generator import LootGenerator
from src.core.targetable_interface import Targetable
from src.data.data_manager import DataManager
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
                 data_manager: DataManager,
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
        self.action_logger = ActionLogger()
        self.turn_logger = EventLogger(self)
        self.num_rounds = 0
        self.winning_side = []  # List[CombatTeam] The teams who won, for rendering purposes.
        self.losing_side = []
        self.data_manager = data_manager

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

    @property
    def previous_round_actions(self) -> List[Action]:
        return self.action_logger.previous_round_actions

    def is_awaiting_request(self, player) -> bool:
        """
        Are we waiting for somebody to make a move?
        True if there is somebody who still needs to make a move, and that person is not the player arg.
        This is for display purposes.
        """
        awaiting = self.awaiting_team_owners()
        return len(awaiting) > 0 and player not in awaiting

    def awaiting_team_owners(self) -> List[Character]:
        return [team.owner for team in self.teams if team.owner is not None and self._is_request_needed(team)]

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
        return len(self._get_knockouts()) > 0

    def request_action(self, request: Action) -> None:
        """
        :param request: An Action requested by a CombatTeam/player.
        It may be different from what gets executed and reported,
        eg., if the elemental gets knocked out before it can make a move.
        """
        if self.is_awaiting_knockout_replacements():
            self._add_knockout_replacement(request)
            if len(self.action_requests) == len(self._get_knockouts()):
                self._resolve_requests()
        else:
            self.action_requests.append(request)
            if len(self.action_requests) == len(self.teams):
                self._resolve_requests()

    def get_target(self, ability: Ability, actor: CombatElemental) -> Targetable or None:
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
        elif target == Target.NONE:
            return None
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

    def forfeit(self, team) -> None:
        """
        When a user selects Flee during battle. This can potentially end the match.
        :param team: CombatTeam
        """
        assert team.side is not None
        if team.side == Combat.SIDE_A:
            self.side_a.remove(team)
        elif team.side == Combat.SIDE_B:
            self.side_b.remove(team)
        team.end_combat()
        self._check_combat_end()

    def _add_knockout_replacement(self, request: Action) -> None:
        if isinstance(request, Switch) and request.team in self._get_knockouts():
            self.action_requests.append(request)

    def _resolve_requests(self) -> None:
        """
        When all players have made an action request, resolve the order and execution of those requests.
        """
        kos = []  # List[CombatElemental]: elementals knocked out this turn
        recently_active = [team.active_elemental for team in self.teams if team.active_elemental is not None]
        for action_group in self._get_priority_order_requests():
            for action in self._sort_fastest(action_group):
                self._resolve_request(action)
                self._check_kos(kos)
                self._check_opponent_change(recently_active)
                if self._check_combat_end():
                    return
        for team in self.teams:
            team.end_round()
            self._check_kos(kos)
        self._prepare_new_round()

    @staticmethod
    def _sort_fastest(actions: List[Action]) -> List[Action]:
        return sorted(actions, key=lambda action: action.speed, reverse=True)

    def _check_opponent_change(self, recently_active: List[CombatElemental]) -> None:
        if len(recently_active) == 0:
            return
        for team in self.teams:
            if team.active_elemental not in recently_active or team.active_elemental.is_knocked_out:
                old_active = next(active for active in recently_active if active.team == team)
                for opposing_team in self.get_enemy_side(team):
                    opposing_team.active_elemental.on_opponent_changed(old_active)

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
        exp_gained = from_elemental.level * 6 + 10  # Yes, fairly arbitrary amount...
        for enemy_team in enemy_side:
            if not enemy_team.is_npc:
                enemy_team.add_exp(exp_gained)

    def _resolve_request(self, action: Action) -> None:
        if action.can_execute:
            action.execute()
            self.action_logger.add_log(action)

    def _prepare_new_round(self) -> None:
        self.num_rounds += 1
        self.action_logger.prepare_new_round()
        self.action_requests = []
        self.turn_logger.prepare_new_round()
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

    def _check_combat_end(self) -> bool:
        def is_all_knocked_out(side):
            return all([team.is_all_knocked_out for team in side])

        side_a_lose = is_all_knocked_out(self.side_a) or len(self.side_a) == 0
        side_b_lose = is_all_knocked_out(self.side_b) or len(self.side_b) == 0
        if side_a_lose and not side_b_lose:
            self.winning_side = self.side_b
            self.losing_side = self.side_a
            self._generate_loot()
        elif side_b_lose and not side_a_lose:
            self.winning_side = self.side_a
            self.losing_side = self.side_b
            self._generate_loot()
        if side_a_lose or side_b_lose:
            self._end_combat()
            return True

    def _generate_loot(self) -> None:
        LootGenerator(winning_side=self.winning_side,
                      losing_side=self.losing_side).generate_loot()

    def _end_combat(self) -> None:
        self.in_progress = False
        for team in self.teams:
            team.end_combat()
        self._save_results()
        print(f"Completed battle in {self.num_rounds} rounds.")

    def _save_results(self) -> None:
        for team in self.teams:
            if team.owner and not team.owner.is_npc:
                self.data_manager.save_all(team.owner)

    def _get_knockouts(self):
        """
        :return: List[CombatTeam] Return teams whose active Elemental was knocked out last turn.
        We then wait for them to send out a new one.
        """
        return [team for team in self.teams if team.active_elemental and team.active_elemental.is_knocked_out]

    def _is_request_needed(self, team) -> bool:
        """
        :param team: CombatTeam
        :return: True if we're waiting on this team to make a move.
        """
        team_in_request = any(request.team for request in self.action_requests if request == team)
        if self.is_awaiting_knockout_replacements():
            return team.active_elemental and team.active_elemental.is_knocked_out and team_in_request is None
        return team_in_request is None

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
