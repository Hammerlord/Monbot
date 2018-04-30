from src.elemental.ability.ability import TurnPriority, Target
from src.elemental.status_effect.status_effects.enrage import EnrageEffect


class Enrage:
    """
    An ability that applies Enrage.
    """
    def __init__(self):
        super().__init__()
        self.name = "Enrage"
        self.description = EnrageEffect().description
        self.turn_priority = TurnPriority.NORMAL
        self.mana_cost = 15
        self.targeting = Target.SELF

    @property
    def status_effect(self) -> EnrageEffect:
        return EnrageEffect()