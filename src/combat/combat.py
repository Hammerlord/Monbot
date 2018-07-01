from typing import List

from src.character.character import Character
from src.elemental.ability.ability import Target, Ability
from src.elemental.combat_elemental import CombatElemental


class Combat:
    """
    How two CombatTeams communicate.
    """

    def __init__(self):
        self.__players = []  # The Players participating in the match
        self.__teams = []  # The CombatTeams participating in the match
        self.max_teams = 2
        self.is_started = False

    @property
    def teams(self):
        """
        :return: List[CombatTeam]: Defensive copy
        """
        return self.__teams.copy()

    def join_battle(self, combat_team) -> bool:
        """
        :param combat_team: CombatTeam
        :return bool: True if we were able to join the battle.
        """
        if not self.__can_join_battle(combat_team):
            return False
        self.__teams.append(combat_team)
        combat_team.set_combat(self)
        if combat_team.owner:
            self.__players.append(combat_team.owner)
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

    def get_active_enemy(self, actor: CombatElemental) -> CombatElemental:
        """
        :return: The active CombatElemental that is not currently requesting a target.
        TODO this, of course, doesn't support modes with >2 teams/enemies.
        """
        return next(team.active_elemental for team in self.__teams if team.active_elemental != actor)

    def check_end(self) -> None:
        for team in self.__teams:
            if team.is_all_knocked_out:
                self.end_combat()

    def end_combat(self) -> None:
        self.is_started = False
        for player in self.__players:
            player.is_busy = False

    def is_previous_turn_knockout(self) -> List[Character]:
        """
        Return team owners whose active Elemental was knocked out last turn.
        We then wait for them to send out a new one.
        """
        return [team.owner for team in self.__teams if team.active.is_knocked_out]

    def __can_join_battle(self, combat_team) -> bool:
        return (len(self.__teams) < self.max_teams and
                combat_team not in self.__teams and
                not self.is_started)
