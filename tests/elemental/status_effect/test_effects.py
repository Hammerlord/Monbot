from src.elemental.status_effect.status_effect import StatusEffect


class GenericBuff(StatusEffect):
    def __init__(self):
        super().__init__()
        self._id = 1
        self._name = "Strength buff"
        self._description = "Increases physical attack."
        self._max_duration = self._calculate_duration(num_turns=3)
        self.refresh_duration()

    def on_effect_start(self):
        self.apply_stat_changes()

    def apply_stat_changes(self) -> None:
        self._update_p_att_stages(2)

    def get_recap(self) -> str:
        return f"{self._target.nickname}'s physical attack has greatly increased!"


class PermaBuff(StatusEffect):
    def __init__(self):
        super().__init__()
        self._id = 2
        self._name = "Rainfall"
        self._description = "Increases magic defence."
        self._max_duration = self._calculate_duration(num_turns=-1)  # No duration
        self.is_dispellable = False
        self.ends_on_switch = False

    def on_effect_start(self):
        self.apply_stat_changes()

    def apply_stat_changes(self) -> None:
        self._update_m_def_stages(1)

    def get_recap(self) -> str:
        return f"{self._target.nickname}'s magic defence has increased."
