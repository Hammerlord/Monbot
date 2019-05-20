from typing import List

from src.elemental.elemental import Elemental
from src.elemental.species.npc_monsters.manapher import Manapher
from src.team.team import Team
from tests.character.character_builder import PlayerBuilder
from tests.elemental.elemental_builder import ElementalBuilder


class TeamBuilder:
    def __init__(self):
        self._owner = PlayerBuilder().with_elementals([]).build()
        self._elementals = [ElementalBuilder().with_species(Manapher()).build()]

    def with_owner(self, owner) -> 'TeamBuilder':
        """
        :param owner: Player or NPC
        """
        self._owner = owner
        return self

    def with_elementals(self, elementals: List[Elemental]) -> 'TeamBuilder':
        self._elementals = elementals
        return self

    def build(self) -> Team:
        return Team(self._owner, self._elementals)
