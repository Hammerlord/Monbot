from src.character.consumables import Meat
from src.character.materials import EarthShard, ManaShard
from src.core.elements import Elements
from src.elemental.ability.ability_factory import LearnableAbilities
from src.elemental.species.species import Species, Stats, Loot


class Rex(Species):
    def __init__(self):
        super().__init__()
        self._name = 'Rex'
        self._description = 'The mountains awoke when their charge granted them a portion of her life force.'
        self._element = Elements.EARTH
        self._left_icon = ':rhino:'
        self._right_icon = ':rhino:'
        self._portrait = None
        self._loot = [Loot(EarthShard(), 0.75),
                      Loot(Meat(), 0.8),
                      Loot(ManaShard(), 0.2)]
        self._learnable_abilities = [LearnableAbilities.slam(),
                                     LearnableAbilities.charge(),
                                     LearnableAbilities.enrage(4),
                                     LearnableAbilities.rampage(9),
                                     LearnableAbilities.rend(14),
                                     LearnableAbilities.quake(18),
                                     LearnableAbilities.fireball(23),
                                     LearnableAbilities.stormbolt(28),
                                     LearnableAbilities.counter(33)]

    @property
    def growth_rate(self) -> 'GrowthRate':
        return GrowthRate()


class GrowthRate(Stats):

    def __init__(self):
        super().__init__()
        self._max_hp = 6
        self._physical_att = 4
        self._magic_att = 4
        self._physical_def = 6
        self._magic_def = 5
        self._speed = 3
        self._base_damage = 1

