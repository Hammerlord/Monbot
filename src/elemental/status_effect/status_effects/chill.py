from src.core.constants import FROST
from src.elemental.status_effect.status_effect import StatusEffect, EffectType
from src.elemental.status_effect.status_effects.freeze import Freeze


class Chill(StatusEffect):
    def __init__(self):
        super().__init__()
        self.effect_type = EffectType.CHILL
        self.name = "Chill"
        self._description = ("Reduces enemy physical attack and speed. "
                             "Freezes the enemy on the fifth application, and stacks reset to 1.")
        self.icon = FROST
        self.max_stacks = 5

    @property
    def turn_duration(self):
        return -1

    @property
    def application_recap(self) -> str:
        return f"{self.target.nickname} has been chilled!"

    def apply_stat_changes(self) -> None:
        self._update_p_att_stages(-1)
        self._update_speed_stages(-1)

    def _on_add_stack(self) -> None:
        if self.current_stacks == self.max_stacks:
            freeze = Freeze()
            freeze.applier = self.applier
            self.target.add_status_effect(freeze)
            self.reset_stacks()
