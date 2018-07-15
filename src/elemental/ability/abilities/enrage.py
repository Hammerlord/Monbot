from src.core.constants import ENRAGE
from src.elemental.ability.ability import TurnPriority, Target, Ability
from src.elemental.status_effect.status_effects.enrage import EnrageEffect


class Enrage(Ability):
    """
    An ability that applies Enrage.
    """
    def __init__(self):
        super().__init__()
        self.name = "Enrage"
        self._description = EnrageEffect().description
        self.turn_priority = TurnPriority.NORMAL
        self.icon = ENRAGE
        self.mana_cost = 15
        self.targeting = Target.SELF

    @property
    def status_effect(self) -> EnrageEffect:
        return EnrageEffect()
