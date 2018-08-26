from src.core.constants import DEFEND
from src.elemental.ability.ability import Ability, Target, TurnPriority
from src.elemental.status_effect.status_effects.defend import DefendEffect


class Defend(Ability):
    """
    An ability that applies Defend.
    """
    def __init__(self):
        super().__init__()
        self.name = "Defend"
        self._description = "Block incoming damage until the next round."
        self.icon = DEFEND
        self.turn_priority = TurnPriority.DEFEND
        self.targeting = Target.SELF
        self.defend_cost = 1

    @property
    def status_effect(self) -> DefendEffect:
        return DefendEffect()
