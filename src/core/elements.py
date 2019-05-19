from enum import Enum
from typing import List
from src.core.constants import DARK, LIGHT, WIND, EARTH, FIRE, WATER, LIGHTNING, CHAOS


class Elements(Enum):
    """
    Element typing for Elementals and Abilities.
    """

    NONE = 0
    LIGHTNING = 1
    WATER = 2
    FIRE = 3
    EARTH = 4
    WIND = 5
    LIGHT = 6
    DARK = 7
    CHAOS = 8

    @staticmethod
    def get_icon(element) -> str:
        icon_map = {
            Elements.LIGHTNING: LIGHTNING,
            Elements.WATER: WATER,
            Elements.FIRE: FIRE,
            Elements.EARTH: EARTH,
            Elements.WIND: WIND,
            Elements.LIGHT: LIGHT,
            Elements.DARK: DARK,
            Elements.CHAOS: CHAOS
        }
        if element in icon_map:
            return icon_map[element]
        return ''


class Category(Enum):
    """
    Physical or magic.
    """

    NONE = 0
    PHYSICAL = 1
    MAGIC = 2


class Effectiveness:
    """
    Compares two elements, and checks if one is effective, normal, or not very effective against the other.
    """

    def __init__(self,
                 to_check: Elements,
                 against: Elements):
        """
        :param to_check: The element to check the in/effectiveness...
        :param against: ... against this element.
        """
        self.to_check = to_check
        self.against = against

    @staticmethod
    def find_effective(comparators: List,
                       against_element: Elements) -> List:
        """
        Given a list of CombatElementals or Abilities, return the ones
        that are *effective* against a target element, if any.
        """
        return [comparator for comparator in comparators if
                Effectiveness(comparator.element, against_element).is_effective()]

    @staticmethod
    def find_neutral(comparators: List,
                     against_element: Elements) -> List:
        """
        Given a list of CombatElementals or Abilities, return the ones
        that are at least *neutral* against a target element, if any.
        """
        return [comparator for comparator in comparators if not
        Effectiveness(comparator.element, against_element).is_resistant()]

    def calculate_multiplier(self) -> int:
        effectiveness_multiplier = 1  # 1 = normal, <1 = resisted, >1 = effective
        if self.is_effective():
            effectiveness_multiplier += 0.5
        elif self.is_resistant():
            effectiveness_multiplier -= 0.5
        return effectiveness_multiplier

    def is_resistant(self) -> bool:
        # Is the ability not very effective against the target's element?
        # Chaos has no resistances.
        return (self.__check_elements(self.against, self.to_check) or
                self.__is_same_element())

    def is_effective(self) -> bool:
        """
        "Is the ability super effective against the target's element?"
        Chaos is weak to and effective against all elements.
        """
        return (self.__check_elements(self.to_check, self.against) or
                self.__is_light_vs_dark(self.to_check, self.against) or
                self.__is_chaos(self.to_check, self.against))

    def __is_same_element(self) -> bool:
        return (self.to_check == self.against and
                self.to_check != Elements.CHAOS)

    @staticmethod
    def __check_elements(to_check: Elements, against: Elements) -> bool:
        if against == Elements.LIGHTNING:
            # Lightning is weak against earth and fire.
            return to_check == Elements.EARTH or to_check == Elements.FIRE
        if against == Elements.WATER:
            # Water is weak against lightning and wind.
            return to_check == Elements.LIGHTNING or to_check == Elements.WIND
        if against == Elements.FIRE:
            # Fire is weak against water and wind.
            return to_check == Elements.WATER or to_check == Elements.WIND
        if against == Elements.EARTH:
            # Earth is weak against water and fire.
            return to_check == Elements.WATER or to_check == Elements.FIRE
        if against == Elements.WIND:
            # Wind is weak against lightning and earth.
            return to_check == Elements.LIGHTNING or to_check == Elements.EARTH

    @staticmethod
    def __is_light_vs_dark(to_check: Elements, against: Elements) -> bool:
        """
        Light and dark are effective against each other.
        """
        if against == Elements.LIGHT:
            # Light is weak against dark.
            return to_check == Elements.DARK
        if against == Elements.DARK:
            # Dark is weak against light.
            return to_check == Elements.LIGHT

    @staticmethod
    def __is_chaos(against: Elements, to_check: Elements) -> bool:
        return against == Elements.CHAOS or to_check == Elements.CHAOS
