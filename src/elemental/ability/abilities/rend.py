from src.core.elements import Elements, Category
from src.elemental.ability.ability import Ability, Target, TurnPriority
from src.elemental.status_effect.status_effects.bleeds import RendEffect


class Rend(Ability):
    def __init__(self):
        super().__init__()
        self.name = "Rend"
        self._description = (f"Inflict a {self.status_effect.attack_power} attack power " 
                             f"bleed that lasts for {self.status_effect.turn_duration} turns.")
        self.element = Elements.WIND
        self.category = Category.PHYSICAL
        self.attack_power = 2
        self.mana_cost = 3
        self.defend_cost = 0
        self.targeting = Target.ENEMY_CLEAVE

    @property
    def status_effect(self) -> RendEffect:
        return RendEffect()
