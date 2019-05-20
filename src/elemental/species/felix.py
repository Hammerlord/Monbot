

from src.core.elements import Elements
from src.elemental.ability.ability_factory import LearnableAbilities
from src.elemental.species.species import Stats, Species


class Felix(Species):

    def __init__(self):
        super().__init__()
        self._name = 'Felix'
        self._description = ('An aquatic twin-tailed fox with an uncanny ability to sense people in distress.'
                             'It is said to come to the aid of the lost.')
        self._element = Elements.WATER
        self._growth_rate = GrowthRate()
        self._left_icon = ':fox:'
        self._right_icon = ':fox:'
        self._portrait = None
        self._learnable_abilities = [LearnableAbilities.slam(),
                                     LearnableAbilities.blessed_rain(),
                                     LearnableAbilities.geyser(5),
                                     LearnableAbilities.windrush(10),
                                     LearnableAbilities.gale_step(15),
                                     LearnableAbilities.cyclone(20),
                                     LearnableAbilities.deluge(25),
                                     LearnableAbilities.frost_barrier(30),
                                     LearnableAbilities.icy_snap(35)]

    @property
    def growth_rate(self) -> 'GrowthRate':
        return GrowthRate()


class GrowthRate(Stats):
    def __init__(self):
        super().__init__()
        self._max_hp = 4.5
        self._physical_att = 4
        self._magic_att = 4
        self._physical_def = 4
        self._magic_def = 5
        self._speed = 6
        self._base_damage = 1
