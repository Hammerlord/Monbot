from src.elemental.status_effect.status_effect import StatusEffect


class EnrageEffect(StatusEffect):
    def __init__(self):
        super().__init__()
        self._name = "Enraged!"
        self.num_turns = 3
        self._description = f"Gain physical and magic attack every turn for {self.num_turns}."
        self._max_duration = self._calculate_duration(self.num_turns)
        self.refresh_duration()

    def on_effect_start(self) -> None:
        self.apply_stat_changes()

    def on_turn_start(self) -> str:
        return f"{self.target.nickname}'s rage increases."

    def apply_stat_changes(self) -> None:
        stages = (self.max_duration - self.duration_remaining) // 2
        self._update_p_att_stages(stages)
        self._update_m_att_stages(stages)