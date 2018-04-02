from enum import Enum
from typing import List


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


class StatsInterface:

    """
    Getter properties for classes that implement the main 5 stats:
    Physical attack, magic attack, physical defence, magic defence, speed.
    """

    def __init__(self):
        self._physical_att = 0
        self._magic_att = 0
        self._physical_def = 0
        self._magic_def = 0
        self._speed = 0

    @property
    def physical_att(self) -> int:
        return self._physical_att

    @property
    def magic_att(self) -> int:
        return self._magic_att

    @property
    def physical_def(self) -> int:
        return self._physical_def

    @property
    def magic_def(self) -> int:
        return self._magic_def

    @property
    def speed(self) -> int:
        return self._speed


class GrowthRate(StatsInterface):

    """
    How much of each stat an Elemental of a specific Species is supposed to gain per level.
    """

    def __init__(self):
        super().__init__()
        self._hp = 3
        self._physical_att = 2
        self._magic_att = 2
        self._physical_def = 2
        self._magic_def = 2
        self._speed = 1

    @property
    def hp(self) -> int:
        return self._hp


class Species(StatsInterface):

    """
    Static information used to set up a level 1 Elemental.
    """

    def __init__(self):
        super().__init__()
        self._name = 'Anonymous Species'
        self._element = Elements.NONE
        self._max_hp = 50
        self._starting_mana = 20
        self._max_mana = 50
        self._growth_rate = GrowthRate()
        self._abilities = []  # List[LearnableAbility]. TBD by descendants.

    @property
    def name(self) -> str:
        return self._name

    @property
    def element(self) -> Elements:
        """
        :return: An enumerated int pertaining to this Species' element.
        """
        return self._element

    @property
    def growth_rate(self) -> GrowthRate:
        """
        Must be overridden to customize the stat growth!
        """
        raise NotImplementedError

    @property
    def learnable_abilities(self) -> List['LearnableAbility']:
        return self._abilities

    @property
    def max_hp(self) -> int:
        return self._max_hp

    @property
    def starting_mana(self) -> int:
        return self._starting_mana

    @property
    def max_mana(self) -> int:
        return self._max_mana