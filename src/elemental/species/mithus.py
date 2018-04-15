from src.core.elements import Elements
from src.elemental.species.species import Species, StatsInterface


class GrowthRate(StatsInterface):

    def __init__(self):
        super().__init__()
        self._max_hp = 4
        self._physical_att = 2
        self._magic_att = 3
        self._physical_def = 3
        self._magic_def = 4
        self._speed = 3


class Mithus(Species):
    def __init__(self):
        super().__init__()
        self._name = 'Mithus'
        self._description = 'Avatar of water'
        self._element = Elements.WATER
        self._max_hp = 55
        self._starting_mana = 20
        self._max_mana = 50
        self._physical_att = 16
        self._magic_att = 17
        self._physical_def = 17
        self._magic_def = 16
        self._speed = 14
        self._mana_per_turn = 5
        self._defend_charges = 2
        self._left_icon = ':whale2:'
        self._right_icon = ':whale2:'
        self._portrait = None
        self._growth_rate = GrowthRate()
        self._learnable_abilities = []