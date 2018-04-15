from src.team.team import Team
from tests.character.character_builder import PlayerBuilder


class TeamBuilder:
    def __init__(self):
        self._owner = PlayerBuilder().with_elementals([]).build()

    def with_owner(self, owner) -> 'TeamBuilder':
        """
        :param owner: Player or NPC
        """
        self._owner = owner
        return self

    def build(self) -> Team:
        return Team(self._owner)
