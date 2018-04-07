from typing import List

from src.core.elements import Elements


class StatsInterface:

    """
    Getter properties for classes that implement the main 5 stats:
    Physical attack, magic attack, physical defence, magic defence, speed.
    """

    def __init__(self):
        self._max_hp = 0
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

    @property
    def max_hp(self) -> int:
        return self._max_hp


class GrowthRate(StatsInterface):

    """
    How much of each stat an Elemental of a specific Species is supposed to gain per level.
    """

    def __init__(self):
        super().__init__()
        self._max_hp = 3
        self._physical_att = 3
        self._magic_att = 3
        self._physical_def = 3
        self._magic_def = 3
        self._speed = 3


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
        self._mana_per_turn = 5
        self._defend_charges = 2
        self._growth_rate = GrowthRate()  # Must be overridden to customize the stat growth!
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
        return self._growth_rate

    @property
    def learnable_abilities(self) -> List['LearnableAbility']:
        return self._abilities

    @property
    def starting_mana(self) -> int:
        return self._starting_mana

    @property
    def max_mana(self) -> int:
        return self._max_mana

    @property
    def mana_per_turn(self) -> int:
        return self._mana_per_turn

    @property
    def defend_charges(self) -> int:
        return self._defend_charges