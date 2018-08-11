from src.character.consumables import Peach
from src.character.materials import ManaShard, WindShard
from src.core.elements import Elements
from src.elemental.ability.ability_factory import LearnableAbilities
from src.elemental.species.species import Stats, Species, Loot


class Slyfe(Species):
    def __init__(self):
        super().__init__()
        self._name = 'Slyfe'
        self._description = 'Avatar of the Wind'
        self._element = Elements.WIND
        self._left_icon = ':dove:'
        self._right_icon = ':dove:'
        self._portrait = None
        self._loot = [Loot(WindShard(), 0.75),
                      Loot(Peach(), 0.8),
                      Loot(ManaShard(), 0.2)]
        self._learnable_abilities = [LearnableAbilities.slam(),
                                     LearnableAbilities.cyclone(),
                                     LearnableAbilities.windrush(4),
                                     LearnableAbilities.gale_step(8),
                                     LearnableAbilities.stormbolt(12),
                                     LearnableAbilities.blessed_rain(16)]

    @property
    def growth_rate(self) -> 'GrowthRate':
        return GrowthRate()


class GrowthRate(Stats):

    def __init__(self):
        super().__init__()
        self._max_hp = 5
        self._physical_att = 5
        self._magic_att = 4
        self._physical_def = 4
        self._magic_def = 4
        self._speed = 5
        self._base_damage = 1
