from src.character.consumables import Cake, Pudding, Peach
from src.character.materials import WaterShard, ManaShard
from src.core.elements import Elements
from src.elemental.ability.ability_factory import LearnableAbilities
from src.elemental.species.species import StatsInterface, Species, Loot


class GrowthRate(StatsInterface):
    def __init__(self):
        super().__init__()
        self._max_hp = 3
        self._physical_att = 2
        self._magic_att = 2
        self._physical_def = 2
        self._magic_def = 2
        self._speed = 3


class Felix(Species):
    def __init__(self):
        super().__init__()
        self._name = 'Felix'
        self._description = ('An aquatic twin-tailed fox with an uncanny ability to sense people in distress.'
                             'It is said to come to the aid of the lost.')
        self._element = Elements.WATER
        self._max_hp = 55
        self._starting_mana = 20
        self._max_mana = 50
        self._physical_att = 11
        self._magic_att = 11
        self._physical_def = 13
        self._magic_def = 13
        self._speed = 20
        self._mana_per_turn = 5
        self._defend_charges = 2
        self._left_icon = ':fox:'
        self._right_icon = ':fox:'
        self._portrait = None
        self._growth_rate = GrowthRate()
        self._loot = [Loot(Peach(), 0.75),
                      Loot(WaterShard(), 0.5),
                      Loot(Cake(), 0.5),
                      Loot(Pudding(), 0.2),
                      Loot(ManaShard(), 0.1)]
        self._learnable_abilities = [LearnableAbilities.slam(),
                                     LearnableAbilities.blessed_rain(),
                                     LearnableAbilities.geyser(5),
                                     LearnableAbilities.windrush(10),
                                     LearnableAbilities.gale_step(15),
                                     LearnableAbilities.cyclone(20),
                                     LearnableAbilities.deluge(25),
                                     LearnableAbilities.frost_barrier(30),
                                     LearnableAbilities.icy_snap(35)]
