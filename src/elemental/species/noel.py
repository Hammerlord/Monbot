from src.character.consumables import Meat, Pudding
from src.character.materials import WaterShard, ManaShard
from src.core.elements import Elements
from src.elemental.ability.ability_factory import LearnableAbilities
from src.elemental.species.species import Stats, Species, Loot


class Noel(Species):
    def __init__(self):
        super().__init__()
        self._name = 'Noel'
        self._description = ('A great ice-aspected warg. Ancient Eldorian legend states '
                             'that it will appear to the one destined to rule.')
        self._element = Elements.WATER
        self._left_icon = ':wolf:'
        self._right_icon = ':wolf:'
        self._portrait = None
        self._loot = [Loot(WaterShard(), 0.75),
                      Loot(Meat(), 0.5),
                      Loot(ManaShard(), 0.2),
                      Loot(Pudding(), 0.1)]
        self._learnable_abilities = [LearnableAbilities.reap(),
                                     LearnableAbilities.razor_fangs(),
                                     LearnableAbilities.geyser(4),
                                     LearnableAbilities.blood_fangs(8),
                                     LearnableAbilities.rend(12),
                                     LearnableAbilities.gale_step(17),
                                     LearnableAbilities.windrush(22),
                                     LearnableAbilities.frost_barrier(25),
                                     LearnableAbilities.deluge(27),
                                     LearnableAbilities.icy_snap(32),
                                     LearnableAbilities.counter(37)]

    @property
    def growth_rate(self) -> 'GrowthRate':
        return GrowthRate()


class GrowthRate(Stats):

    def __init__(self):
        super().__init__()
        self._max_hp = 4.5
        self._physical_att = 5
        self._magic_att = 5
        self._physical_def = 4
        self._magic_def = 4
        self._speed = 4
        self._base_damage = 1
