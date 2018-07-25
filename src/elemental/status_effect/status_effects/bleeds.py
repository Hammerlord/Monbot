from src.core.constants import BLEED
from src.core.elements import Category
from src.elemental.ability.damage_calculator import DamageCalculator
from src.elemental.status_effect.status_effect import StatusEffect, EffectType


class Bleed(StatusEffect):

    def __init__(self):
        super().__init__()
        self.effect_type = EffectType.BLEED
        self.category = Category.PHYSICAL
        self.attack_power = 1
        self.icon = BLEED

    @property
    def turn_duration(self) -> int:
        return 4

    def on_turn_end(self) -> bool:
        damage_calculator = DamageCalculator(self.target, self.applier, self)
        damage_calculator.calculate()
        damage = damage_calculator.final_damage
        self.target.receive_damage(damage, self.applier)
        return True

    @property
    def application_recap(self) -> str:
        return f'{self.target.nickname} has been wounded!'

    @property
    def trigger_recap(self) -> str:
        source = self.name if self.name else "its wounds"
        return f'{self.target.nickname} was hurt by {source}.'


class RazorFangsEffect(Bleed):

    def __init__(self):
        super().__init__()
        self.attack_power = 12
        self.name = "Razor Fangs"


class RendEffect(Bleed):

    def __init__(self):
        super().__init__()
        self.attack_power = 15
        self.name = "Rend"

    @property
    def turn_duration(self) -> int:
        return 3
