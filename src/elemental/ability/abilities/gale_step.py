from src.core.constants import GALESTEP
from src.core.elements import Elements, Category
from src.elemental.ability.ability import Ability, TurnPriority, Target
from src.elemental.status_effect.status_effects.gale_step import GaleStepEffect


class GaleStep(Ability):
    def __init__(self):
        super().__init__()
        self.name = "Gale Step"
        self._description = f"Increase speed significantly for {self.status_effect.turn_duration} turns."
        self.element = Elements.WIND
        self.icon = GALESTEP
        self.category = Category.NONE
        self.attack_power = 0
        self.mana_cost = 10
        self.defend_cost = 0
        self.turn_priority = TurnPriority.NORMAL
        self.targeting = Target.SELF

    @property
    def status_effect(self) -> GaleStepEffect:
        return GaleStepEffect()
