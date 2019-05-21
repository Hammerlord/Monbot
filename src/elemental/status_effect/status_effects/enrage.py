from src.core.constants import ENRAGE
from src.elemental.status_effect.status_effect import StatusEffect


class EnrageEffect(StatusEffect):
    def __init__(self):
        super().__init__()
        self.name = "Enraged!"
        self._description = (f"Increase physical and magic attack by 1 stage "
                             f"every turn for {self.turn_duration} turns.")
        self.icon = ENRAGE
        self.uptime = 0  # The number of turns this effect has been up.

    @property
    def p_att_stages(self) -> int:
        return self.uptime

    @property
    def m_att_stages(self) -> int:
        return self.uptime

    @property
    def turn_duration(self):
        return 3

    def on_turn_end(self):
        if self.turns_remaining > 0:
            self.uptime += 1

    def on_effect_start(self):
        self.uptime = 0

    @property
    def fade_recap(self) -> str:
        return f"{self.target.nickname}'s rage fades."