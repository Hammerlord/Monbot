from src.core.elements import Category
from src.elemental.ability.damage_calculator import DamageCalculator
from src.elemental.status_effect.status_effect import StatusEffect, EffectType


class Bleed(StatusEffect):

    def __init__(self):
        super().__init__()
        self.effect_type = EffectType.BLEED
        self.category = Category.PHYSICAL
        self.base_power = 1

    @property
    def _base_duration(self) -> float:
        return 4

    def on_turn_end(self):
        damage_calculator = DamageCalculator(self.target, self.applier, self)
        damage_calculator.calculate()
        damage = damage_calculator.final_damage
        self.target.receive_damage(damage, self.applier)


class RendEffect(Bleed):

    def __init__(self):
        super().__init__()
        self.base_power = 5

    @property
    def _base_duration(self) -> float:
        return 3
