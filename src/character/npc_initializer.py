import random

from src.character.npc import NPC
from src.elemental.species.felix import Felix
from src.elemental.species.mithus import Mithus
from src.elemental.species.nepharus import Nepharus
from src.elemental.species.noel import Noel
from src.elemental.species.npc_monsters.manapher import Manapher
from src.elemental.species.rainatu import Rainatu
from src.elemental.species.rex import Rex
from src.elemental.species.roaus import Roaus
from src.elemental.species.sithel import Sithel
from src.elemental.species.slyfe import Slyfe


class NPCInitializer:

    def create_opponent(self, character) -> NPC:
        """
        Creates a level-appropriate opponent for the character.
        :param character: The character to match against.
        :return:
        """
        opponent = self.get_random_opponent()
        opponent.generate_team(character)
        return opponent

    def get_random_opponent(self) -> NPC:
        opponents = [self.adventurer,
                     self.researcher,
                     self.explorer]
        pick = random.randint(0, len(opponents) - 1)
        return opponents[pick]()

    @staticmethod
    def adventurer() -> NPC:
        potential_species = [Mithus(), Roaus(), Rainatu(), Sithel()]
        return NPC('Adventurer',
                   potential_species)

    @staticmethod
    def collector() -> NPC:
        potential_species = [Mithus(), Roaus(), Rainatu(), Sithel(),
                             Felix(), Manapher(), Nepharus(), Slyfe(), Noel(), Rex()]
        return NPC('Collector',
                   potential_species)

    @staticmethod
    def researcher() -> NPC:
        pass

    @staticmethod
    def explorer() -> NPC:
        pass

    @staticmethod
    def archaeologist() -> NPC:
        pass

    @staticmethod
    def cultist() -> NPC:
        pass

    @staticmethod
    def paladin() -> NPC:
        pass

    @staticmethod
    def enforcer() -> NPC:
        pass