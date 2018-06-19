from typing import List

from src.character.character import Character
from src.elemental.ability.ability import Target, Ability
from src.elemental.combat_elemental import CombatElemental


class Combat:

    """
    How two CombatTeams communicate.
    """

    def __init__(self):
        self.players = []  # The Players participating in the match
        self.teams = []  # The CombatTeams participating in the match

    def join_battle(self, combat_team) -> None:
        """
        :param combat_team: CombatTeam
        """
        self.teams.append(combat_team)
        combat_team.set_combat(self)
        if combat_team.owner:
            self.players.append(combat_team.owner)

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
        """
        return next(team.active_elemental for team in self.teams if team.active_elemental != actor)

    def check_end(self) -> None:
        for team in self.teams:
            if team.is_all_knocked_out:
                self.end_combat()

    def end_combat(self) -> None:
        for player in self.players:
            player.is_busy = False

    def is_previous_turn_knockout(self) -> List[Character]:
        """
        Return team owners whose active Elemental was knocked out last turn.
        We then wait for them to send out a new one.
        """
        return [team.owner for team in self.teams if team.active.is_knocked_out]