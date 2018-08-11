from typing import List

from src.core.elements import Elements


class Stats:

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
        self._base_damage = 0

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

    @property
    def base_damage(self) -> int:
        return self._base_damage


class Species(Stats):

    """
    Static information used to set up a level 1 Elemental.
    """

    def __init__(self):
        super().__init__()
        self._name = 'Anonymous Species'
        self._description = 'Something interesting here.'
        self._element = Elements.NONE
        self._max_hp = 50 + self.growth_rate.max_hp
        self._physical_att = 20 + self.growth_rate.physical_att
        self._magic_att = 20 + self.growth_rate.magic_att
        self._physical_def = 20 + self.growth_rate.physical_def
        self._magic_def = 20 + self.growth_rate.magic_def
        self._speed = 20 + self.growth_rate.speed
        self._starting_mana = 15
        self._max_mana = 50
        self._mana_per_turn = 5
        self._bench_mana_per_turn = 2
        self._defend_charges = 2
        self._base_damage = 10  # How much base damage this Species does at level 1.
        self._left_icon = ''  # This Elemental's emote, facing right.
        self._right_icon = ''  # This Elemental's emote, facing left.
        self._portrait = None
        self._learnable_abilities = []  # List[LearnableAbility]. TBD by descendants.
        self._loot = []  # Items that this species can drop.

    @property
    def left_icon(self) -> str:
        return self._left_icon

    @property
    def right_icon(self) -> str:
        return self._right_icon

    @property
    def name(self) -> str:
        return self._name

    def __str__(self) -> str:
        return self.name

    @property
    def description(self) -> str:
        return self._description

    @property
    def element(self) -> Elements:
        """
        :return: An enumerated int pertaining to this Species' element.
        """
        return self._element

    @property
    def growth_rate(self) -> 'Stats':
        """
        How much of each stat the Elemental is supposed to gain per level.
        """
        raise NotImplementedError

    @property
    def learnable_abilities(self):
        """
        :return: List[LearnableAbility]
        """
        return self._learnable_abilities.copy()

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
    def bench_mana_per_turn(self) -> int:
        return self._bench_mana_per_turn

    @property
    def defend_charges(self) -> int:
        return self._defend_charges

    @property
    def loot(self) -> List['Loot']:
        return list(self._loot)


class Loot:
    """
    An item dropped by an Elemental upon knock-out.
    """
    def __init__(self,
                 item,
                 drop_rate: float=1):
        """
        :param item: Item
        :param drop_rate: The percentage chance that this item will drop upon combat resolution.
        """
        self.item = item
        self.drop_rate = drop_rate
