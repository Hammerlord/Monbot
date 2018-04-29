from src.core.elements import Elements, Category
from src.elemental.ability.ability import Ability, Target, TurnPriority
from src.elemental.status_effect.status_effects.bleeds import RendEffect


class Rend(Ability):
    def __init__(self):
        super().__init__()
        self.name = "Rend"
        self.description = "Rend the enemy, inflicting a bleed for 3 turns."
        self.id = 5
        self.element = Elements.WIND
        self.category = Category.PHYSICAL
        self.base_power = 1
        self.mana_cost = 15
        self.defend_cost = 0
        self.turn_priority = TurnPriority.NORMAL
        self.targeting = Target.ENEMY

    @property
    def status_effect(self) -> RendEffect:
        return RendEffect()
