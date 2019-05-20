from src.core.constants import SPAGHETTI
from src.core.elements import Elements
from src.elemental.ability.ability_factory import LearnableAbilities
from src.elemental.species.species import Species, Stats


class Sithel(Species):
    def __init__(self):
        super().__init__()
        self._name = 'Sithel'
        self._description = 'Falcon lord'
        self._element = Elements.FIRE
        self._left_icon = SPAGHETTI
        self._right_icon = SPAGHETTI
        self._portrait = None
        self._learnable_abilities = [LearnableAbilities.claw(),
                                     LearnableAbilities.enrage(),
                                     LearnableAbilities.fireball(4),
                                     LearnableAbilities.ignite(8),
                                     LearnableAbilities.gale_step(15),
                                     LearnableAbilities.inferno(25)]

    @property
    def growth_rate(self) -> 'GrowthRate':
        return GrowthRate()


class GrowthRate(Stats):

    def __init__(self):
        super().__init__()
        self._max_hp = 4
        self._physical_att = 6
        self._magic_att = 6
        self._physical_def = 4
        self._magic_def = 4
        self._speed = 5
        self._base_damage = 1

