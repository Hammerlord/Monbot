from src.core.elements import Elements
from src.elemental.ability.ability_factory import LearnableAbilities
from src.elemental.species.species import StatsInterface, Species


class GrowthRate(StatsInterface):

    def __init__(self):
        super().__init__()
        self._max_hp = 3
        self._physical_att = 3
        self._magic_att = 2
        self._physical_def = 1
        self._magic_def = 3
        self._speed = 2


class Nepharus(Species):
    def __init__(self):
        super().__init__()
        self._name = 'Nepharus'
        self._description = ('A jet-black serpent with baleful eyes. It'
                             'resides in the far recesses of the cosmos.')
        self._element = Elements.DARK
        self._max_hp = 55
        self._starting_mana = 20
        self._max_mana = 50
        self._physical_att = 11
        self._magic_att = 14
        self._physical_def = 10
        self._magic_def = 13
        self._speed = 10
        self._mana_per_turn = 5
        self._defend_charges = 2
        self._left_icon = ':tophat:'
        self._right_icon = ':tophat:'
        self._portrait = None
        self._growth_rate = GrowthRate()
        self._learnable_abilities = [LearnableAbilities.razor_fangs(),
                                     LearnableAbilities.reap(),
                                     LearnableAbilities.blood_fangs(5),
                                     LearnableAbilities.rend(10),
                                     LearnableAbilities.black_pinion(15)]
