from src.core.elements import Elements
from src.elemental.ability.ability_factory import LearnableAbilities
from src.elemental.species.species import Species, StatsInterface


class GrowthRate(StatsInterface):

    def __init__(self):
        super().__init__()
        self._max_hp = 2
        self._physical_att = 3
        self._magic_att = 4
        self._physical_def = 3
        self._magic_def = 3
        self._speed = 4


class Sithel(Species):
    def __init__(self):
        super().__init__()
        self._name = 'Sithel'
        self._description = 'Falcon lord'
        self._element = Elements.FIRE
        self._max_hp = 50
        self._starting_mana = 20
        self._max_mana = 50
        self._physical_att = 14
        self._magic_att = 14
        self._physical_def = 9
        self._magic_def = 8
        self._speed = 15
        self._mana_per_turn = 5
        self._defend_charges = 2
        self._left_icon = ':spaghetti:'
        self._right_icon = ':spaghetti:'
        self._portrait = None
        self._growth_rate = GrowthRate()
        self._learnable_abilities = [LearnableAbilities.claw(),
                                     LearnableAbilities.enrage(),
                                     LearnableAbilities.fireball(2)]
