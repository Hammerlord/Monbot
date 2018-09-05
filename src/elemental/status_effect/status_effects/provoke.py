from src.core.constants import PROVOKE
from src.elemental.status_effect.status_effect import StatusEffect, EffectType


class ProvokeEffect(StatusEffect):
    def __init__(self):
        super().__init__()
        self.icon = PROVOKE
        self.effect_type = EffectType.SWITCH_PREVENTION
        self.max_stacks = 5
        self.ends_on_applier_changed = True

    @property
    def turn_duration(self):
        return 5

    @property
    def application_recap(self) -> str:
        return f"{self.target.nickname} has been taunted."

    def apply_stat_changes(self) -> None:
        self._update_p_def_stages(-1)
