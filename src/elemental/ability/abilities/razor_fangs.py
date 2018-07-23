from src.core.elements import Elements, Category
from src.elemental.ability.ability import Ability, Target, TurnPriority
from src.elemental.status_effect.status_effects.bleeds import RazorFangsEffect


class RazorFangs(Ability):
    def __init__(self):
        super().__init__()
        self.name = "Razor Fangs"
        self._description = f"Slash the enemy, inflicting a bleed for {self.status_effect.turn_duration} turns."
        self.element = Elements.NONE
        self.category = Category.PHYSICAL
        self.base_power = 0
        self.mana_cost = 10
        self.defend_cost = 0
        self.turn_priority = TurnPriority.NORMAL
        self.targeting = Target.ENEMY

    @property
    def status_effect(self) -> RazorFangsEffect:
        return RazorFangsEffect()
