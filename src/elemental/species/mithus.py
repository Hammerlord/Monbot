from src.core.elements import Elements
from src.elemental.ability.ability_factory import LearnableAbilities
from src.elemental.species.species import Species, StatsInterface


class GrowthRate(StatsInterface):

    def __init__(self):
        super().__init__()
        self._max_hp = 4
        self._physical_att = 2
        self._magic_att = 3
        self._physical_def = 2
        self._magic_def = 3
        self._speed = 1


class Mithus(Species):
    def __init__(self):
        super().__init__()
        self._name = 'Mithus'
        self._description = 'Avatar of water'
        self._element = Elements.WATER
        self._max_hp = 55
        self._starting_mana = 20
        self._max_mana = 50
        self._physical_att = 11
        self._magic_att = 14
        self._physical_def = 10
        self._magic_def = 13
        self._speed = 10
        self._mana_per_turn = 5
        self._defend_charges = 2
        self._left_icon = ':whale2:'
        self._right_icon = ':whale2:'
        self._portrait = None
        self._growth_rate = GrowthRate()
        self._learnable_abilities = [LearnableAbilities.razor_fangs(),
                                     LearnableAbilities.claw(),
                                     LearnableAbilities.geyser(4)]
