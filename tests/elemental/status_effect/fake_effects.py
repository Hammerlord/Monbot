from src.elemental.status_effect.status_effect import StatusEffect


class GenericBuff(StatusEffect):
    def __init__(self):
        super().__init__()
        self._id = 1
        self._name = "Strength buff"
        self._description = "Increases physical attack."

    @property
    def p_att_stages(self) -> int:
        return 2

    @property
    def turn_duration(self) -> int:
        return 7

    def on_effect_start(self):
        super().on_effect_start()
        return f"{self.target.nickname}'s physical attack has greatly increased!"


class PermaBuff(StatusEffect):
    def __init__(self):
        super().__init__()
        self._id = 2
        self._name = "Rainfall"
        self._description = "Increases magic defence."
        self.is_dispellable = False
        self.ends_on_switch = False

    @property
    def m_def_stages(self) -> int:
        return 1

    @property
    def turn_duration(self) -> int:
        return -1

    def on_effect_start(self) -> str:
        super().on_effect_start()
        return f"{self.target.nickname}'s magic defence has increased."
