from src.core.elements import Elements, Category
from src.elemental.ability.ability import Ability, TurnPriority, Target
from src.elemental.status_effect.status_effects.burns import IgniteEffect


class Ignite(Ability):
    def __init__(self):
        super().__init__()
        self.name = "Ignite"
        self._description = f"Set enemies on fire for {self.status_effect.turn_duration} turns."
        self.element = Elements.FIRE
        self.category = Category.MAGIC
        self.attack_power = 5
        self.mana_cost = 3
        self.defend_cost = 0
        self.turn_priority = TurnPriority.NORMAL
        self.targeting = Target.ENEMY_AOE

    @property
    def status_effect(self) -> IgniteEffect:
        return IgniteEffect()
