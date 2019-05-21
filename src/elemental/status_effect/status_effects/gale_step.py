from src.core.constants import GALESTEP
from src.elemental.status_effect.status_effect import StatusEffect


class GaleStepEffect(StatusEffect):
    def __init__(self):
        super().__init__()
        self.name = "Gale Step"
        self._description = f"Increase speed significantly for {self.turn_duration} turns."
        self.icon = GALESTEP
        self.max_stacks = 3

    @property
    def speed_stages(self) -> int:
        return 2

    @property
    def turn_duration(self):
        return 5

    @property
    def application_recap(self) -> str:
        return f"{self.target.nickname}'s speed rose greatly!"
