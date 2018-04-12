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
        self._target.update_physical_att(25)

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
        self.fades_on_switch = False

    def on_effect_start(self):
        self.apply_stat_changes()

    def apply_stat_changes(self) -> None:
        self._target.update_magic_def(10)

    def get_recap(self) -> str:
        return f"{self._target.nickname}'s magic defence has increased."