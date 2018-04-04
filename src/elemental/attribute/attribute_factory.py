from random import randint
from typing import List, Type

from src.elemental.attribute.attribute import Attribute, Ferocity, Resolve, Sturdiness, Swiftness, Resistance, \
    Attunement
from src.elemental.attribute.attribute_manager import AttributeManager


class AttributeFactory:

    @staticmethod
    def get_potential_attributes() -> List[Type[Attribute]]:
        """
        :return: References to all the Attribute subclasses.
        """
        return [
            Ferocity,
            Sturdiness,
            Resolve,
            Attunement,
            Resistance,
            Swiftness
        ]

    @staticmethod
    def get_random_attributes() -> List[Type[Attribute]]:
        """
        :return: References to three random Attribute subclasses.
        """
        attribute_pool = AttributeFactory.get_potential_attributes()

        def get_random_attribute() -> Type[Attribute]:
            pick = randint(0, len(attribute_pool) - 1)
            return attribute_pool.pop(pick)

        return [get_random_attribute() for i in range(3)]

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
        attributes = AttributeFactory.get_random_attributes()
        return AttributeFactory.create_preset_manager(attributes)

    @staticmethod
    def create_preset_manager(attributes: List[Type[Attribute]]) -> AttributeManager:
        """
        :param attributes: A list of Attribute references.
        """
        manager = AttributeManager()
        for attribute in attributes:
            attribute(manager)
            manager.add_attribute(attribute)
        return manager

    @staticmethod
    def ferocity() -> Type[Attribute]:
        """
        :return: Physical attack Attribute.
        """
        return Ferocity

    @staticmethod
    def sturdiness() -> Type[Attribute]:
        """
        :return: Physical defence Attribute.
        """
        return Sturdiness

    @staticmethod
    def resolve() -> Type[Attribute]:
        """
        :return: Max HP Attribute.
        """
        return Resolve

    @staticmethod
    def attunement() -> Type[Attribute]:
        """
        :return: Magic attack Attribute.
        """
        return Attunement

    @staticmethod
    def resistance() -> Type[Attribute]:
        """
        :return: Magic defence Attribute.
        """
        return Resistance

    @staticmethod
    def swiftness() -> Type[Attribute]:
        """
        :return: Speed Attribute.
        """
        return Swiftness

    @staticmethod
    def add_ferocity(manager: AttributeManager):
        attribute = Ferocity(manager)
        manager.add_attribute(attribute)

    @staticmethod
    def add_sturdiness(manager: AttributeManager):
        attribute = Sturdiness(manager)
        manager.add_attribute(attribute)

    @staticmethod
    def add_resolve(manager: AttributeManager):
        attribute = Resolve(manager)
        manager.add_attribute(attribute)

    @staticmethod
    def add_attunement(manager: AttributeManager):
        attribute = Attunement(manager)
        manager.add_attribute(attribute)

    @staticmethod
    def add_resistance(manager: AttributeManager):
        attribute = Resistance(manager)
        manager.add_attribute(attribute)

    @staticmethod
    def add_swiftness(manager: AttributeManager):
        attribute = Swiftness(manager)
        manager.add_attribute(attribute)