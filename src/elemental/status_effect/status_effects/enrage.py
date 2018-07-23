from src.core.constants import ENRAGE
from src.elemental.status_effect.status_effect import StatusEffect


class EnrageEffect(StatusEffect):
    def __init__(self):
        super().__init__()
        self.name = "Enraged!"
        self._description = f"Gain physical and magic attack every turn for {self.turn_duration} turns."
        self.icon = ENRAGE
        self.uptime = 0  # The number of turns this effect has been up.

    @property
    def turn_duration(self):
        return 3

    def on_turn_end(self) -> bool:
        if self.turns_remaining > 0:
            self.uptime += 1
            return True

    @property
    def trigger_recap(self) -> str:
        return f"{self.target.nickname}'s rage increases."

    @property
    def fade_recap(self) -> str:
        return f"{self.target.nickname}'s rage fades."

    def apply_stat_changes(self) -> None:
        stages = self.uptime
        self._update_p_att_stages(stages)
        self._update_m_att_stages(stages)