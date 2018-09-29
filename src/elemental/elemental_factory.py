import random
from typing import List

from src.data.resources import ElementalResource, AttributeResource
from src.elemental.attribute.attribute_factory import AttributeFactory
from src.elemental.elemental import Elemental
from src.elemental.species.felix import Felix
from src.elemental.species.mithus import Mithus
from src.elemental.species.nepharus import Nepharus
from src.elemental.species.noel import Noel
from src.elemental.species.npc_monsters.manapher import Manapher
from src.elemental.species.npc_monsters.tophu import Tophu
from src.elemental.species.rainatu import Rainatu
from src.elemental.species.rex import Rex
from src.elemental.species.roaus import Roaus
from src.elemental.species.sithel import Sithel
from src.elemental.species.slyfe import Slyfe


class ElementalInitializer:
    """
    Factory methods for creating specific Elementals.
    """

    SUMMONABLE_SPECIES = [Mithus(),
                          Roaus(),
                          Rainatu(),
                          Sithel(),
                          Felix(),
                          Nepharus(),
                          Slyfe(),
                          Noel(),
                          Rex()]

    ALL_SPECIES = SUMMONABLE_SPECIES + [
        Manapher(),
        Tophu()
    ]

    NAME_MAP = {}
    for species in ALL_SPECIES:
        NAME_MAP[species.name] = species

    @staticmethod
    def make(species, level=1) -> Elemental:
        """
        :param species: Which subclass of Species
        :param level: How much to level up the Elemental
        """
        elemental = Elemental(species,
                              AttributeFactory.create_random())
        elemental.level_to(level)
        return elemental

    @staticmethod
    def from_server(resource: ElementalResource) -> Elemental:
        species_name = resource.species
        species = ElementalInitializer.NAME_MAP[species_name]
        attributes = [AttributeResource(**attribute) for attribute in resource.attributes]
        elemental = Elemental(species,
                              AttributeFactory.create_from_resources(attributes),
                              id=resource.id)
        elemental.load_from_resource(resource)
        return elemental

    @staticmethod
    def make_random(level=1, excluding: List[Elemental] = None) -> Elemental:
        """
        :param level: The desired level of the Elemental.
        :param excluding: A List[Species] of elementals to exclude.
        :return:
        """
        if excluding:
            excluded_species = [elemental.species.name for elemental in excluding]
            potential_species = [species for species in ElementalInitializer.SUMMONABLE_SPECIES
                                 if species.name not in excluded_species]
        else:
            potential_species = ElementalInitializer.SUMMONABLE_SPECIES
        pick = random.randint(0, len(potential_species) - 1)
        return ElementalInitializer.make(potential_species[pick], level)


def print_abilities():
    for species in ElementalInitializer.SUMMONABLE_SPECIES:
        print(species.name)
        for learnable in species.learnable_abilities:
            print(f"Lv. {learnable.level_required} {learnable.name} "
                  f"[{learnable.element} {learnable.category}]\n"
                  f"Mana cost: {learnable.mana_cost}  Power: {learnable.attack_power}\n"
                  f"{learnable.description}\n")
        print('\n')

# print_abilities()
