from enum import Enum


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


class Category(Enum):

    """
    Physical or magic.
    """

    NONE = 0
    PHYSICAL = 1
    MAGIC = 2


class Effectiveness:

    """
    Checks if the attack is effective, normal, or not very effective.
    """

    def __init__(self,
                 ability_element: Elements,
                 target_element: Elements):
        """
        :param ability_element: The element of the Ability being used
        :param target_element: The element of the CombatElemental recipient
        """
        self.ability_element = ability_element
        self.target_element = target_element
        self.effectiveness_multiplier = 1  # 1 = normal, <1 = resisted, >1 = effective

    def calculate(self) -> int:
        if self.__is_effective():
            self.effectiveness_multiplier += 0.5
        if self.__is_resistant():
            self.effectiveness_multiplier -= 0.5
        return self.effectiveness_multiplier

    def __is_resistant(self) -> bool:
        # Is the ability not very effective against the target's element?
        # Chaos has no resistances.
        return self.__check_elements(self.ability_element, self.target_element) or \
               (self.ability_element == self.target_element and self.ability_element != Elements.CHAOS)

    def __is_effective(self) -> bool:
        """
        "Is the ability super effective against the target's element?"
        Chaos is weak to and effective against all elements.
        """
        return self.__check_elements(self.target_element, self.ability_element) or \
               self.__is_light_vs_dark(self.target_element, self.ability_element) or \
               self.__is_chaos(self.target_element, self.ability_element)

    @staticmethod
    def __check_elements(against: Elements, to_check: Elements) -> bool:
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
    def __is_light_vs_dark(against: Elements, to_check: Elements) -> bool:
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
