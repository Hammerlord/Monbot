

from src.core.constants import PINEAPPLE
from src.core.elements import Elements
from src.elemental.ability.ability_factory import LearnableAbilities
from src.elemental.species.species import Species, Stats


class Rainatu(Species):
    def __init__(self):
        super().__init__()
        self._name = 'Rainatu'
        self._description = 'Not a pineapple.'
        self._element = Elements.LIGHTNING
        self._left_icon = PINEAPPLE
        self._right_icon = PINEAPPLE
        self._portrait = None
        self._growth_rate = GrowthRate()
        self._learnable_abilities = [LearnableAbilities.slam(),
                                     LearnableAbilities.rolling_thunder(),
                                     LearnableAbilities.stormbolt(4),
                                     LearnableAbilities.windrush(8),
                                     LearnableAbilities.recharge(12),
                                     LearnableAbilities.gale_step(16),
                                     LearnableAbilities.aurora(25)]

    @property
    def growth_rate(self) -> 'GrowthRate':
        return GrowthRate()


class GrowthRate(Stats):

    def __init__(self):
        super().__init__()
        self._max_hp = 5
        self._physical_att = 4
        self._magic_att = 5
        self._physical_def = 4
        self._magic_def = 5
        self._speed = 6
        self._base_damage = 1
