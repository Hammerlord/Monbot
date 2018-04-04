from random import randint
from typing import List, Type

from src.elemental.attribute.attribute import Attribute, Ferocity, Resolve, Sturdiness, Swiftness, Resistance, \
    Attunement
from src.elemental.attribute.attribute_manager import AttributeManager


class AttributeFactory:

    @staticmethod
    def get_potential_attributes() -> List[Attribute]:
        """
        :return: Attribute subclasses.
        """
        return [
            Ferocity(),
            Sturdiness(),
            Resolve(),
            Attunement(),
            Resistance(),
            Swiftness()
        ]

    @staticmethod
    def create_empty_manager() -> AttributeManager:
        """
        :return: An AttributeManager with an empty Attribute list.
        """
        return AttributeManager()

    @staticmethod
    def create_manager() -> AttributeManager:
        """
        :return: An AttributeManager with three random Attributes.
        """
        manager = AttributeManager()
        attribute_pool = AttributeFactory.get_potential_attributes()
        for i in range(3):
            pick = randint(0, len(attribute_pool) - 1)
            attribute = attribute_pool.pop(pick)
            manager.add_attribute(attribute)
        return manager

    @staticmethod
    def add_ferocity(manager: AttributeManager) -> None:
        manager.add_attribute(Ferocity())

    @staticmethod
    def add_sturdiness(manager: AttributeManager) -> None:
        manager.add_attribute(Sturdiness())

    @staticmethod
    def add_resolve(manager: AttributeManager) -> None:
        manager.add_attribute(Resolve())

    @staticmethod
    def add_attunement(manager: AttributeManager) -> None:
        manager.add_attribute(Attunement())

    @staticmethod
    def add_resistance(manager: AttributeManager) -> None:
        manager.add_attribute(Resistance())

    @staticmethod
    def add_swiftness(manager: AttributeManager) -> None:
        manager.add_attribute(Swiftness())