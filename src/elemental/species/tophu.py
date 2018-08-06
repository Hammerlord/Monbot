from src.character.consumables import Peach, ManaShard
from src.core.elements import Elements
from src.elemental.ability.ability_factory import LearnableAbilities
from src.elemental.species.species import Species, StatsInterface, Loot


class GrowthRate(StatsInterface):

    def __init__(self):
        super().__init__()
        self._max_hp = 3
        self._physical_att = 1
        self._magic_att = 2
        self._physical_def = 2
        self._magic_def = 4
        self._speed = 2


class Tophu(Species):
    """
    An NPC elemental that's meant to be an easy enemy.
    """
    def __init__(self):
        super().__init__()
        self._name = 'Tophu'
        self._description = 'A lesser elemental, also called an elemental mote.'
        self._element = Elements.LIGHT
        self._max_hp = 50
        self._starting_mana = 20
        self._max_mana = 50
        self._physical_att = 5
        self._magic_att = 5
        self._physical_def = 20
        self._magic_def = 20
        self._speed = 10
        self._mana_per_turn = 5
        self._defend_charges = 2
        self._left_icon = '✨'
        self._right_icon = '✨'
        self._portrait = None
        self._growth_rate = GrowthRate()
        self._learnable_abilities = [LearnableAbilities.claw(),
                                     LearnableAbilities.slam()]
        self._loot = [Loot(Peach()),
                      Loot(ManaShard())]
