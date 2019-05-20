
from src.core.constants import OX
from src.core.elements import Elements
from src.elemental.ability.ability_factory import LearnableAbilities
from src.elemental.species.species import Species, Stats


class Roaus(Species):
    def __init__(self):
        super().__init__()
        self._name = 'Roaus'
        self._description = 'A horse with a thousand hammers'
        self._element = Elements.EARTH
        self._left_icon = OX
        self._right_icon = OX
        self._portrait = None
        self._learnable_abilities = [LearnableAbilities.charge(),
                                     LearnableAbilities.slam(),
                                     LearnableAbilities.windrush(4),
                                     LearnableAbilities.quake(8),
                                     LearnableAbilities.counter(12),
                                     LearnableAbilities.stonehide(16)]

    @property
    def growth_rate(self) -> 'GrowthRate':
        return GrowthRate()


class GrowthRate(Stats):

    def __init__(self):
        super().__init__()
        self._max_hp = 5
        self._physical_att = 4
        self._magic_att = 3
        self._physical_def = 5
        self._magic_def = 4
        self._speed = 4
        self._base_damage = 1

