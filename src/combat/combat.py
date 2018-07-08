from typing import List

from src.character.character import Character
from src.elemental.ability.ability import Target, Ability
from src.elemental.combat_elemental import CombatElemental


class Combat:
    """
    How CombatTeams communicate.
    Two opposing sides to a battlefield are distinguished, internally, by "side_a" and "side_b".
    TODO for now we only have 1v1, even though each side allows multiple CombatTeams to join.
    """

    def __init__(self):
        self.side_a = []  # List[CombatTeam] One side of the battlefield.
        self.side_b = []  # List[CombatTeam] Another side of the battlefield.
        self.max_teams_per_side = 3
        self.in_progress = False

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
        return True

    def get_target(self, ability: Ability, actor: CombatElemental) -> CombatElemental:
        """
        :return: The CombatElemental the Ability should affect, based on the Ability's targeting enum.
        """
        target = ability.targeting
        if target == Target.SELF:
            return actor
        elif target == Target.ENEMY:
            return self.get_active_enemy(actor)

    def get_active_enemy(self, of_elemental: CombatElemental) -> CombatElemental:
        """
        :param of_elemental: The elemental looking for an opponent.
        :return: The first CombatElemental on the opposing side.
        TODO work in progress: this, of course, doesn't support multiple elementals on one side.
        """
        return self.get_opposing_side(of_elemental.team)[0]

    def get_opposing_side(self, combat_team) -> List[CombatElemental]:
        """
        :return: All active CombatElementals on the side opposing the passed-in CombatTeam.
        """
        if any(team == combat_team for team in self.side_b):
            return [team.active_elemental for team in self.side_a]
        if any(team == combat_team for team in self.side_a):
            return [team.active_elemental for team in self.side_b]
        print("??? That CombatTeam isn't a part of this battle.")
        return []

    def check_end(self) -> None:
        if (all(team.is_all_knocked_out for team in self.side_a) or
                all(team.is_all_knocked_out for team in self.side_b)):
            self.end_combat()

    def end_combat(self) -> None:
        self.in_progress = False
        for team in self.teams:
            team.end_combat()

    def is_previous_turn_knockout(self):
        """
        :return: List[CombatTeam] Return teams whose active Elemental was knocked out last turn.
        We then wait for them to send out a new one.
        """
        return [team for team in self.teams if team.active.is_knocked_out]

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
