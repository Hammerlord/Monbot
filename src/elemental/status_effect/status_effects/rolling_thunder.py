from src.core.constants import ROLLING_THUNDER
from src.core.elements import Elements, Category
from src.elemental.ability.damage_calculator import DamageCalculator
from src.elemental.status_effect.status_effect import StatusEffect


class RollingThunderEffect(StatusEffect):
    """
    A debuff that eventually detonates for damage.
    """
    def __init__(self):
        super().__init__()
        self._description = f"Detonates after 1 turn."
        self.name = "Rolling Thunder"
        self.icon = ROLLING_THUNDER
        self.element = Elements.LIGHTNING
        self.category = Category.MAGIC
        self.base_power = 20
        self.can_add_instances = True

    @property
    def turn_duration(self):
        return 2

    def on_turn_end(self) -> bool:
        if self.turns_remaining == 1:
            damage_calculator = DamageCalculator(self.target, self.applier, self)
            damage = damage_calculator.calculate()
            self.target.receive_damage(damage, self.applier)
            return True

    @property
    def trigger_recap(self) -> str:
        return f'{self.name} crackles with energy on {self.target.nickname}!'

    @property
    def application_recap(self) -> str:
        return f'Dark clouds gather over {self.target.nickname}.'
