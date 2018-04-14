from src.team.team import Team
from tests.character.test_user import UserBuilder


class TeamBuilder:
    def __init__(self):
        self._owner = UserBuilder().build()

    def with_owner(self, owner) -> 'TeamBuilder':
        """
        :param owner: Player or NPC
        """
        self._owner = owner
        return self

    def build(self) -> Team:
        return Team(self._owner)
