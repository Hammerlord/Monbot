from src.core.constants import FIRE
from src.core.elements import Category
from src.elemental.ability.damage_calculator import DamageCalculator
from src.elemental.status_effect.status_effect import StatusEffect, EffectType


class Burn(StatusEffect):

    def __init__(self):
        super().__init__()
        self.name = 'Burn'
        self.icon = FIRE
        self.effect_type = EffectType.BURN
        self.category = Category.MAGIC  # Are all burns magical? Maybe?
        self.attack_power = 1

    @property
    def turn_duration(self) -> float:
        return 4

    def on_turn_end(self) -> bool:
        damage_calculator = DamageCalculator(self.target, self.applier, self)
        damage_calculator.calculate()
        damage = damage_calculator.final_damage
        self.target.receive_damage(damage, self.applier)
        return True

    @property
    def application_recap(self) -> str:
        return f'{self.target.nickname} has been burned!'

    @property
    def trigger_recap(self) -> str:
        return f'{self.target.nickname} was hurt by its burn.'


class IgniteEffect(Burn):

    def __init__(self):
        super().__init__()
        self.attack_power = 2

    @property
    def turn_duration(self) -> float:
        return 5
