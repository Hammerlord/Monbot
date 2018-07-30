from src.core.elements import Elements
from src.elemental.ability.ability_factory import LearnableAbilities
from src.elemental.species.species import StatsInterface, Species


class GrowthRate(StatsInterface):

    def __init__(self):
        super().__init__()
        self._max_hp = 2
        self._physical_att = 3
        self._magic_att = 3
        self._physical_def = 2
        self._magic_def = 2
        self._speed = 2


class Noel(Species):
    def __init__(self):
        super().__init__()
        self._name = 'Noel'
        self._description = ('A great ice-aspected warg. Ancient Eldorian legend states '
                             'that it will appear to the one destined to rule.')
        self._element = Elements.WATER
        self._max_hp = 55
        self._starting_mana = 20
        self._max_mana = 50
        self._physical_att = 14
        self._magic_att = 14
        self._physical_def = 10
        self._magic_def = 10
        self._speed = 13
        self._mana_per_turn = 5
        self._defend_charges = 2
        self._left_icon = ':wolf:'
        self._right_icon = ':wolf:'
        self._portrait = None
        self._growth_rate = GrowthRate()
        self._learnable_abilities = [LearnableAbilities.reap(),
                                     LearnableAbilities.razor_fangs(),
                                     LearnableAbilities.geyser(4),
                                     LearnableAbilities.blood_fangs(8),
                                     LearnableAbilities.rend(12),
                                     LearnableAbilities.gale_step(17),
                                     LearnableAbilities.windrush(22),
                                     LearnableAbilities.deluge(27),
                                     LearnableAbilities.counter(32)]
