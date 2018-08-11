from src.character.consumables import Peach, Cake
from src.character.materials import ManaShard
from src.core.elements import Elements
from src.elemental.ability.ability_factory import LearnableAbilities
from src.elemental.species.species import Stats, Species, Loot


class Nepharus(Species):
    def __init__(self):
        super().__init__()
        self._name = 'Nepharus'
        self._description = ('A jet-black serpent with baleful eyes. It'
                             'resides in the far recesses of the cosmos.')
        self._element = Elements.DARK
        self._left_icon = ':tophat:'
        self._right_icon = ':tophat:'
        self._portrait = None
        self._loot = [Loot(Peach(), 0.8),
                      Loot(Cake(), 0.3),
                      Loot(ManaShard(), 0.3)]
        self._learnable_abilities = [LearnableAbilities.razor_fangs(),
                                     LearnableAbilities.reap(),
                                     LearnableAbilities.blood_fangs(5),
                                     LearnableAbilities.rend(10),
                                     LearnableAbilities.black_pinion(15),
                                     LearnableAbilities.geyser(20),
                                     LearnableAbilities.quake(25),
                                     LearnableAbilities.dissonant_roar(30),
                                     LearnableAbilities.howling_dark(35)]

    @property
    def growth_rate(self) -> 'GrowthRate':
        return GrowthRate()


class GrowthRate(Stats):

    def __init__(self):
        super().__init__()
        self._max_hp = 5
        self._physical_att = 4
        self._magic_att = 4
        self._physical_def = 3
        self._magic_def = 5
        self._speed = 4
        self._base_damage = 1
