from src.elemental.status_effect.status_effect import StatusEffect


class PAttBuff(StatusEffect):
    def __init__(self):
        super().__init__()
        self._name = "Physical Attack+"
        self._description = f"Increases physical attack by 1 stage."
        self.can_add_instances = True

    @property
    def turn_duration(self) -> int:
        return 7

    @property
    def trigger_recap(self) -> str:
        return f"{self.target.nickname}'s physical attack has increased."

    def apply_stat_changes(self) -> None:
        self._update_p_att_stages(1)


class PAttBuffLarge(StatusEffect):
    def __init__(self):
        super().__init__()
        self._name = "Physical Attack++"
        self.num_turns = 3
        self._description = f"Increases physical attack by 2 stages."
        self.can_add_instances = True

    @property
    def turn_duration(self) -> int:
        return 3

    @property
    def trigger_recap(self) -> str:
        return f"{self.target.nickname}'s physical attack has greatly increased!"

    def apply_stat_changes(self) -> None:
        self._update_p_att_stages(2)
