from src.character.consumables import Peach, Cake
from src.character.materials import LightningShard, ManaShard
from src.core.elements import Elements
from src.elemental.ability.ability_factory import LearnableAbilities
from src.elemental.species.species import Species, StatsInterface, Loot


class GrowthRate(StatsInterface):

    def __init__(self):
        super().__init__()
        self._max_hp = 2
        self._physical_att = 2
        self._magic_att = 3
        self._physical_def = 2
        self._magic_def = 3
        self._speed = 2


class Rainatu(Species):
    def __init__(self):
        super().__init__()
        self._name = 'Rainatu'
        self._description = 'Not a pineapple.'
        self._element = Elements.LIGHTNING
        self._max_hp = 50
        self._starting_mana = 20
        self._max_mana = 50
        self._physical_att = 10
        self._magic_att = 14
        self._physical_def = 8
        self._magic_def = 14
        self._speed = 14
        self._mana_per_turn = 5
        self._defend_charges = 2
        self._left_icon = ':pineapple:'
        self._right_icon = ':pineapple:'
        self._portrait = None
        self._growth_rate = GrowthRate()
        self._loot = [Loot(LightningShard(), 0.75),
                      Loot(Peach(), 0.8),
                      Loot(ManaShard(), 0.2),
                      Loot(Cake(), 0.3)]
        self._learnable_abilities = [LearnableAbilities.slam(),
                                     LearnableAbilities.rolling_thunder(),
                                     LearnableAbilities.stormbolt(4),
                                     LearnableAbilities.windrush(8),
                                     LearnableAbilities.gale_step(15)]
