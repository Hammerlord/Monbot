
from src.core.elements import Elements
from src.elemental.ability.ability_factory import LearnableAbilities
from src.elemental.species.species import Species, Stats


class Tophu(Species):
    """
    An NPC elemental that's meant to be an easy enemy.
    """
    def __init__(self):
        super().__init__()
        self._name = 'Tophu'
        self._description = 'A lesser elemental, also called an elemental mote.'
        self._element = Elements.LIGHT
        self._left_icon = '✨'
        self._right_icon = '✨'
        self._portrait = None
        self._learnable_abilities = [LearnableAbilities.claw(),
                                     LearnableAbilities.slam()]

    @property
    def growth_rate(self) -> 'GrowthRate':
        return GrowthRate()


class GrowthRate(Stats):

    def __init__(self):
        super().__init__()
        self._max_hp = 5
        self._physical_att = 4
        self._magic_att = 4
        self._physical_def = 5
        self._magic_def = 4
        self._speed = 4
        self._base_damage = 1
