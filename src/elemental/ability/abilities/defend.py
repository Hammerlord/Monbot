from src.elemental.ability.ability import Ability, Target
from src.elemental.status_effect.status_effects.defend import DefendEffect


class Defend(Ability):
    """
    An ability that applies Defend.
    """
    def __init__(self):
        super().__init__()
        self.id = 1
        self.name = "Defend"
        self.description = "Block incoming damage until the next turn. Gain +10 mana."
        self.turn_priority = 2
        self.targeting = Target.SELF

    @property
    def status_effect(self) -> DefendEffect:
        return DefendEffect()
