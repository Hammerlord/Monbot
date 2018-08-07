from src.character.consumables import Peach
from src.character.materials import ManaShard, WindShard
from src.core.elements import Elements
from src.elemental.ability.ability_factory import LearnableAbilities
from src.elemental.species.species import StatsInterface, Species, Loot


class GrowthRate(StatsInterface):

    def __init__(self):
        super().__init__()
        self._max_hp = 2
        self._physical_att = 3
        self._magic_att = 2
        self._physical_def = 3
        self._magic_def = 2
        self._speed = 2


class Slyfe(Species):
    def __init__(self):
        super().__init__()
        self._name = 'Slyfe'
        self._description = 'Avatar of the Wind'
        self._element = Elements.WIND
        self._max_hp = 50
        self._starting_mana = 20
        self._max_mana = 50
        self._physical_att = 14
        self._magic_att = 12
        self._physical_def = 12
        self._magic_def = 12
        self._speed = 14
        self._mana_per_turn = 5
        self._defend_charges = 2
        self._left_icon = ':dove:'
        self._right_icon = ':dove:'
        self._portrait = None
        self._growth_rate = GrowthRate()
        self._loot = [Loot(WindShard(), 0.75),
                      Loot(Peach(), 0.8),
                      Loot(ManaShard(), 0.2)]
        self._learnable_abilities = [LearnableAbilities.slam(),
                                     LearnableAbilities.cyclone(),
                                     LearnableAbilities.windrush(4),
                                     LearnableAbilities.gale_step(8)]
