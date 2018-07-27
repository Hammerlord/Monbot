from src.elemental.status_effect.status_effect import StatusEffect


class GaleStepEffect(StatusEffect):
    def __init__(self):
        super().__init__()
        self.name = "Gale Step"
        self._description = f"Increase speed significantly for {self.turn_duration} turns."
        self.icon = ':dash:'

    @property
    def turn_duration(self):
        return 4

    @property
    def application_recap(self) -> str:
        return f"{self.target.nickname}'s speed rose!"

    def apply_stat_changes(self) -> None:
        self._update_speed_stages(2)