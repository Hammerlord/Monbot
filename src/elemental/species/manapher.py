from src.character.consumables import Peach, ManaShard
from src.core.elements import Elements
from src.elemental.ability.ability_factory import LearnableAbilities
from src.elemental.species.species import Species, StatsInterface, Loot


class GrowthRate(StatsInterface):

    def __init__(self):
        super().__init__()
        self._max_hp = 2
        self._physical_att = 1
        self._magic_att = 3
        self._physical_def = 3
        self._magic_def = 4
        self._speed = 1


class Manapher(Species):
    """
    An NPC elemental that's meant to be a relatively easy enemy.
    """
    def __init__(self):
        super().__init__()
        self._name = 'Manapher'
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
        self._left_icon = ':koala:'
        self._right_icon = ':koala:'
        self._portrait = None
        self._growth_rate = GrowthRate()
        self._learnable_abilities = [LearnableAbilities.claw(),
                                     LearnableAbilities.shining_laser()]
        self._loot = [Loot(Peach()),
                      Loot(ManaShard())]