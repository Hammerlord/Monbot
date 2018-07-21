from src.core.constants import ROLLING_THUNDER
from src.core.elements import Elements, Category
from src.elemental.ability.damage_calculator import DamageCalculator
from src.elemental.status_effect.status_effect import StatusEffect


class RollingThunderEffect(StatusEffect):
    """
    Detonates on the currently active elemental.
    """
    def __init__(self):
        super().__init__()
        self._description = f"Detonates after 1 round."
        self.name = "Rolling Thunder"
        self.icon = ROLLING_THUNDER
        self.element = Elements.LIGHTNING
        self.category = Category.MAGIC
        self.base_power = 20
        self.can_add_instances = True

    @property
    def _base_duration(self):
        return 1

    def on_turn_end(self) -> bool:
        if self.duration_remaining == 1:
            # This affects a CombatTeam Targetable.
            current_active = self.target.active_elemental
            damage_calculator = DamageCalculator(current_active, self.applier, self)
            damage = damage_calculator.calculate()
            current_active.receive_damage(damage, self.applier)
            return True

    def trigger_recap(self) -> str:
        return f'{self.name} crackles with energy on {self.target.active_elemental.nickname}!'

    def application_recap(self) -> str:
        return f'Dark clouds gather over {self.target.active_elemental.nickname}.'
