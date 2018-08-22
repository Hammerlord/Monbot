from src.core.constants import DISSONANT_ROAR
from src.core.elements import Elements, Category
from src.elemental.status_effect.status_effect import StatusEffect


class DissonantRoarEffect(StatusEffect):

    def __init__(self):
        super().__init__()
        self._description = f"Reduces magic attack by 2 stages for {self.turn_duration} turns."
        self.name = "Rattled"
        self.icon = DISSONANT_ROAR
        self.element = Elements.DARK
        self.category = Category.MAGIC
        self.can_add_instances = True

    @property
    def turn_duration(self) -> int:
        return 5

    @property
    def application_recap(self) -> str:
        return f"{self.target.nickname}'s magic defence fell greatly!"

    def apply_stat_changes(self) -> None:
        self._update_m_def_stages(-2)
