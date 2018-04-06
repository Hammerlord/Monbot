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