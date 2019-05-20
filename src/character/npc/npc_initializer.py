import random
from enum import Enum

from src.character.npc.name_generator import NameGenerator
from src.character.npc.npc import NPC
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


class Professions(Enum):
    ADVENTURER = 'Adventurer'
    COLLECTOR = 'Collector'
    RESEARCHER = 'Researcher'
    ARCHAEOLOGIST = 'Archaeologist'
    PALADIN = 'Paladin'
    ENFORCER = 'Enforcer'
    CULTIST = 'Cultist'
    SCHOLAR = 'Scholar'
    MERCHANT = 'Merchant'
    MAGISTER = 'Magister'
    OVERSEER = 'Overseer'
    WARRIOR = 'Warrior'
    DANCER = 'Dancer'


class NPCInitializer:

    def get_random_opponent(self) -> NPC:
        opponents = [self.adventurer,
                     self.collector]
        pick = random.randint(0, len(opponents) - 1)
        return opponents[pick]()

    @staticmethod
    def make_name_with_title(profession: Professions) -> str:
        return f'{profession} {NameGenerator.generate_name()}'

    @staticmethod
    def adventurer() -> NPC:
        potential_species = [Mithus(), Roaus(), Rainatu(), Sithel()]
        return NPC(NPCInitializer.make_name_with_title(Professions.ADVENTURER),
                   potential_species)

    @staticmethod
    def collector() -> NPC:
        potential_species = [Mithus(), Roaus(), Rainatu(), Sithel(),
                             Felix(), Manapher(), Nepharus(), Slyfe(), Noel(), Rex()]
        return NPC(NPCInitializer.make_name_with_title(Professions.COLLECTOR),
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