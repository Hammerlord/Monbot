from random import randint
from typing import List, Type

from src.data.resources import AttributesResource
from src.elemental.attribute.attribute import Attribute, Ferocity, Resolve, Sturdiness, Swiftness, Resistance, \
    Attunement
from src.elemental.attribute.attribute_manager import AttributeManager


class AttributeFactory:

    POTENTIAL_ATTRIBUTES = [
            Ferocity(),
            Sturdiness(),
            Resolve(),
            Attunement(),
            Resistance(),
            Swiftness()
        ]

    NAME_MAP = {}
    for attribute in POTENTIAL_ATTRIBUTES:
        NAME_MAP[attribute.name] = attribute

    @staticmethod
    def get_potential_attributes() -> List[Attribute]:
        """
        :return: Attribute subclasses. Defensive copy.
        """
        return list(AttributeFactory.POTENTIAL_ATTRIBUTES)

    @staticmethod
    def create_random() -> AttributeManager:
        """
        :return: An AttributeManager with three random Attributes.
        """
        manager = AttributeManager()
        attribute_pool = AttributeFactory.get_potential_attributes()
        for i in range(AttributeManager.MAX_NUM_ATTRIBUTES):
            pick = randint(0, len(attribute_pool) - 1)
            attribute = attribute_pool.pop(pick)
            manager.add_attribute(attribute)
        return manager

    @staticmethod
    def create_from_resources(resources: List[AttributesResource]) -> AttributeManager:
        manager = AttributeManager()
        for resource in resources:
            attribute = AttributeFactory.NAME_MAP[resource.name]
            if attribute:
                manager.add_attribute(attribute)
                attribute.level_to(resource.level)
        assert(len(manager.attributes) == AttributeManager.MAX_NUM_ATTRIBUTES)
        return manager

    @staticmethod
    def create_from_attributes(attribute_names: List[str]) -> AttributeManager:
        manager = AttributeManager()
        for name in attribute_names:
            attribute = AttributeFactory.NAME_MAP[name]
            if attribute:
                manager.add_attribute(attribute)
        assert (len(manager.attributes) == AttributeManager.MAX_NUM_ATTRIBUTES)
        return manager
