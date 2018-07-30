from src.elemental.status_effect.status_effect import StatusEffect


class QuakeEffect(StatusEffect):
    def __init__(self):
        super().__init__()
        self.name = "Quake Slow"
        self._description = f"Decrease speed by 1 stage for {self.turn_duration} turns."
        self.icon = ':turtle:'
        self.max_stacks = 6

    @property
    def turn_duration(self):
        return 3

    @property
    def application_recap(self) -> str:
        return f"{self.target.nickname}'s speed fell."

    def apply_stat_changes(self) -> None:
        self._update_speed_stages(-1)
