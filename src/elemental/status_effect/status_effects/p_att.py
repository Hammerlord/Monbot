from src.elemental.status_effect.status_effect import StatusEffect


class PAttBuff(StatusEffect):
    def __init__(self):
        super().__init__()
        self._id = 1
        self._name = "Physical Attack+"
        self.num_turns = 7
        self._description = f"Increases physical attack by 1 stage. Lasts for {self.num_turns} turns."
        self._max_duration = self._calculate_duration(self.num_turns)
        self.refresh_duration()
        self.can_add_instances = True

    def on_effect_start(self) -> str:
        super().on_effect_start()
        return f"{self.target.nickname}'s physical attack has increased."

    def apply_stat_changes(self) -> None:
        self._update_p_att_stages(1)


class PAttBuffLarge(StatusEffect):
    def __init__(self):
        super().__init__()
        self._id = 2
        self._name = "Physical Attack++"
        self.num_turns = 3
        self._description = f"Increases physical attack by 2 stages. Lasts for {self.num_turns} turns."
        self._max_duration = self._calculate_duration(self.num_turns)
        self.refresh_duration()
        self.can_add_instances = True

    def on_effect_start(self) -> str:
        super().on_effect_start()
        return f"{self.target.nickname}'s physical attack has greatly increased!"

    def apply_stat_changes(self) -> None:
        self._update_p_att_stages(2)
