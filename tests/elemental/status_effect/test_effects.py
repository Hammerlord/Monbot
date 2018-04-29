from src.elemental.status_effect.status_effect import StatusEffect


class GenericBuff(StatusEffect):
    def __init__(self):
        super().__init__()
        self._id = 1
        self._name = "Strength buff"
        self._description = "Increases physical attack."
        self.max_duration = self._calculate_duration(num_turns=3)
        self.refresh_duration()

    def on_effect_start(self):
        super().on_effect_start()
        return f"{self.target.nickname}'s physical attack has greatly increased!"

    def apply_stat_changes(self) -> None:
        self._update_p_att_stages(2)


class PermaBuff(StatusEffect):
    def __init__(self):
        super().__init__()
        self._id = 2
        self._name = "Rainfall"
        self._description = "Increases magic defence."
        self.max_duration = self._calculate_duration(num_turns=-1)  # No duration
        self.is_dispellable = False
        self.ends_on_switch = False

    def on_effect_start(self) -> str:
        super().on_effect_start()
        return f"{self.target.nickname}'s magic defence has increased."

    def apply_stat_changes(self) -> None:
        self._update_m_def_stages(1)
