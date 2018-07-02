from src.elemental.attribute.attribute_factory import AttributeFactory
from src.elemental.elemental import Elemental
from src.elemental.species.mithus import Mithus
from src.elemental.species.rainatu import Rainatu
from src.elemental.species.roaus import Roaus
from src.elemental.species.sithel import Sithel


class ElementalInitializer:

    """
    Factory methods for creating specific Elementals.
    """

    @staticmethod
    def make(species, level=1) -> Elemental:
        """
        :param species: Which subclass of Species
        :param level: How much to level up the Elemental
        """
        elemental = Elemental(species,
                              AttributeFactory.create_manager())
        elemental.level_to(level)
        return elemental

    @staticmethod
    def rainatu(level=1) -> Elemental:
        """
        :return: The lightning starter, Rainatu
        """
        return ElementalInitializer.make(Rainatu(), level)

    @staticmethod
    def roaus(level=1) -> Elemental:
        """
        :return: The earth starter, Roaus
        """
        return ElementalInitializer.make(Roaus(), level)

    @staticmethod
    def mithus(level=1) -> Elemental:
        """
        :return: The water starter, Mithus
        """
        return ElementalInitializer.make(Mithus(), level)

    @staticmethod
    def sithel(level=1) -> Elemental:
        """
        :return: The fire starter, Sithel
        """
        return ElementalInitializer.make(Sithel(), level)
