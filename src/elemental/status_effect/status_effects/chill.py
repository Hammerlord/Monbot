from src.core.constants import FROST
from src.elemental.status_effect.status_effect import StatusEffect, EffectType


class Chill(StatusEffect):
    def __init__(self):
        super().__init__()
        self.effect_type = EffectType.CHILL
        self.name = "Chill"
        self._description = ("Reduces enemy physical attack and speed. "
                             "On the fourth application, they become frozen for 1 turn.")
        self.icon = FROST
        self.max_stacks = 4

    @property
    def turn_duration(self):
        return -1

    @property
    def application_recap(self) -> str:
        return f"{self.target.nickname} has been chilled!"

    def apply_stat_changes(self):
        self._update_p_att_stages(-1)
        self._update_speed_stages(-1)
