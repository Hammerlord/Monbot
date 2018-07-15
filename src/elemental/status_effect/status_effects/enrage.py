from src.core.constants import ENRAGE
from src.elemental.status_effect.status_effect import StatusEffect


class EnrageEffect(StatusEffect):
    def __init__(self):
        super().__init__()
        self._name = "Enraged!"
        self._description = f"Gain physical and magic attack every turn for {self._base_duration} turns."
        self.icon = ENRAGE
        self.uptime = 1  # The number of turns this effect has been up.

    @property
    def _base_duration(self):
        return 3

    def on_effect_start(self) -> None:
        self.apply_stat_changes()

    def on_turn_start(self) -> str:
        self.uptime += 1
        return f"{self.target.nickname}'s rage increases."

    def apply_stat_changes(self) -> None:
        stages = self.uptime
        self._update_p_att_stages(stages)
        self._update_m_att_stages(stages)