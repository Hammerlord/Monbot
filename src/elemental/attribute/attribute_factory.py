from random import randint
from typing import List, Type

from src.elemental.attribute.attribute import Attribute, Ferocity, Resolve, Sturdiness
from src.elemental.attribute.attribute_manager import AttributeManager


class AttributeFactory:

    @staticmethod
    def get_potential_attributes() -> List[Type[Attribute]]:
        return [
            Ferocity,
            Sturdiness,
            Resolve
        ]

    @staticmethod
    def get_random_attributes() -> List[Type[Attribute]]:
        """
        :return: References to the Attribute classes.
        """
        attribute_pool = AttributeFactory.get_potential_attributes()

        def get_random_attribute() -> Type[Attribute]:
            pick = randint(0, len(attribute_pool) - 1)
            return attribute_pool.pop(pick)

        return [get_random_attribute() for i in range(3)]

    @staticmethod
    def create_manager() -> AttributeManager:
        attributes = AttributeFactory.get_random_attributes()
        return AttributeManager(attributes)

    @staticmethod
    def create_manager_from_attributes(attributes) -> AttributeManager:
        """
        :param attributes: A list of Attribute references.
        """
        return AttributeManager(attributes)

    @staticmethod
    def ferocity() -> Type[Attribute]:
        return Ferocity

    @staticmethod
    def sturdiness() -> Type[Attribute]:
        return Sturdiness

    @staticmethod
    def resolve() -> Type[Attribute]:
        return Resolve
