from random import randint
from typing import List, Type

from src.elemental.attribute.attribute import Attribute, Ferocity, Resolve, Sturdiness, Swiftness, Resistance, \
    Attunement
from src.elemental.attribute.attribute_manager import AttributeManager


class AttributeFactory:

    @staticmethod
    def get_potential_attributes(manager: AttributeManager) -> List[Attribute]:
        """
        :return: Attribute subclasses.
        """
        return [
            Ferocity(manager),
            Sturdiness(manager),
            Resolve(manager),
            Attunement(manager),
            Resistance(manager),
            Swiftness(manager)
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
        attribute_pool = AttributeFactory.get_potential_attributes(manager)
        for i in range(3):
            pick = randint(0, len(attribute_pool) - 1)
            attribute = attribute_pool.pop(pick)
            manager.add_attribute(attribute)
        return manager

    @staticmethod
    def add_ferocity(manager: AttributeManager) -> None:
        attribute = Ferocity(manager)
        manager.add_attribute(attribute)

    @staticmethod
    def add_sturdiness(manager: AttributeManager) -> None:
        attribute = Sturdiness(manager)
        manager.add_attribute(attribute)

    @staticmethod
    def add_resolve(manager: AttributeManager) -> None:
        attribute = Resolve(manager)
        manager.add_attribute(attribute)

    @staticmethod
    def add_attunement(manager: AttributeManager) -> None:
        attribute = Attunement(manager)
        manager.add_attribute(attribute)

    @staticmethod
    def add_resistance(manager: AttributeManager) -> None:
        attribute = Resistance(manager)
        manager.add_attribute(attribute)

    @staticmethod
    def add_swiftness(manager: AttributeManager) -> None:
        attribute = Swiftness(manager)
        manager.add_attribute(attribute)