from src.character.consumables import Peach
from src.character.materials import EarthShard, ManaShard
from src.core.elements import Elements
from src.elemental.ability.ability_factory import LearnableAbilities
from src.elemental.species.species import Species, StatsInterface, Loot


class GrowthRate(StatsInterface):

    def __init__(self):
        super().__init__()
        self._max_hp = 2
        self._physical_att = 3
        self._magic_att = 2
        self._physical_def = 3
        self._magic_def = 2
        self._speed = 2


class Roaus(Species):
    def __init__(self):
        super().__init__()
        self._name = 'Roaus'
        self._description = 'A horse with a thousand hammers'
        self._element = Elements.EARTH
        self._max_hp = 55
        self._starting_mana = 20
        self._max_mana = 50
        self._physical_att = 14
        self._magic_att = 8
        self._physical_def = 14
        self._magic_def = 10
        self._speed = 14
        self._mana_per_turn = 5
        self._defend_charges = 2
        self._left_icon = ':ox:'
        self._right_icon = ':ox:'
        self._portrait = None
        self._growth_rate = GrowthRate()
        self._loot = [Loot(EarthShard(), 0.75),
                      Loot(Peach(), 0.8),
                      Loot(ManaShard(), 0.2)]
        self._learnable_abilities = [LearnableAbilities.charge(),
                                     LearnableAbilities.slam(),
                                     LearnableAbilities.windrush(4),
                                     LearnableAbilities.quake(8),
                                     LearnableAbilities.counter(12)]
