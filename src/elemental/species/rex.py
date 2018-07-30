from src.core.elements import Elements
from src.elemental.ability.ability_factory import LearnableAbilities
from src.elemental.species.species import Species, StatsInterface


class GrowthRate(StatsInterface):

    def __init__(self):
        super().__init__()
        self._max_hp = 3
        self._physical_att = 2
        self._magic_att = 2
        self._physical_def = 3
        self._magic_def = 3
        self._speed = 1


class Rex(Species):
    def __init__(self):
        super().__init__()
        self._name = 'Rex'
        self._description = 'The mountains awoke when their charge granted them a portion of her life force.'
        self._element = Elements.EARTH
        self._max_hp = 55
        self._starting_mana = 20
        self._max_mana = 50
        self._physical_att = 12
        self._magic_att = 12
        self._physical_def = 14
        self._magic_def = 14
        self._speed = 8
        self._mana_per_turn = 5
        self._defend_charges = 2
        self._left_icon = ':rhino:'
        self._right_icon = ':rhino:'
        self._portrait = None
        self._growth_rate = GrowthRate()
        self._learnable_abilities = [LearnableAbilities.slam(),
                                     LearnableAbilities.charge(),
                                     LearnableAbilities.enrage(4),
                                     LearnableAbilities.rampage(9),
                                     LearnableAbilities.rend(14),
                                     LearnableAbilities.quake(18),
                                     LearnableAbilities.fireball(23),
                                     LearnableAbilities.stormbolt(28)]
