
from src.core.constants import WHALE
from src.core.elements import Elements
from src.elemental.ability.ability_factory import LearnableAbilities
from src.elemental.species.species import Species, Stats


class Mithus(Species):
    def __init__(self):
        super().__init__()
        self._name = 'Mithus'
        self._description = 'Avatar of water'
        self._element = Elements.WATER
        self._left_icon = WHALE
        self._right_icon = WHALE
        self._portrait = None
        self._learnable_abilities = [LearnableAbilities.razor_fangs(),
                                     LearnableAbilities.claw(),
                                     LearnableAbilities.geyser(4),
                                     LearnableAbilities.frost_barrier(8),
                                     LearnableAbilities.icy_snap(12),
                                     LearnableAbilities.enrage(16),
                                     LearnableAbilities.deluge(25),
                                     LearnableAbilities.dissonant_roar(30)]

    @property
    def growth_rate(self) -> 'GrowthRate':
        return GrowthRate()


class GrowthRate(Stats):

    def __init__(self):
        super().__init__()
        self._max_hp = 5
        self._physical_att = 3
        self._magic_att = 4
        self._physical_def = 5
        self._magic_def = 5
        self._speed = 3
        self._base_damage = 1
