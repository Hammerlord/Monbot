from src.core.constants import STUN
from src.elemental.status_effect.status_effect import StatusEffect, EffectType


class Stun(StatusEffect):
    def __init__(self):
        super().__init__()
        self.effect_type = EffectType.STUN
        self.name = "Stun"
        self._description = "Stunned for 1 turn."
        self.icon = STUN

    @property
    def turn_duration(self):
        return 1

    def on_effect_start(self):
        self.target.cancel_casting()

    @property
    def application_recap(self) -> str:
        return f"{self.target.nickname} is stunned!"
