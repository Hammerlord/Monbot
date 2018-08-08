from src.core.constants import SHELL
from src.elemental.status_effect.status_effect import StatusEffect


class StonehideEffect(StatusEffect):
    def __init__(self):
        super().__init__()
        self.name = "Stonehide"
        self.damage_reduction = 0.3
        self._description = f"Reduces damage taken by {int(self.damage_reduction * 10)}%."
        self.icon = SHELL
        self.charges = 4

    @property
    def turn_duration(self):
        return -1

    @property
    def application_recap(self) -> str:
        return f"{self.target.nickname}'s hide becomes stone, fending oncoming attacks!"

    def apply_stat_changes(self):
        self.target.update_damage_reduction(self.damage_reduction)

    def on_receive_damage(self, amount: int, actor) -> True:
        if amount > 0:
            self.charges -= 1
            if self.charges == 0:
                self.active = False
            return True

    def fade_recap(self) -> str:
        return f"{self.target.nickname}'s Stonehide wore off."
