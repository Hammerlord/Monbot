from src.core.elements import Elements, Category
from src.elemental.status_effect.status_effect import StatusEffect


class Thunderstruck(StatusEffect):

    def __init__(self):
        super().__init__()
        self._description = f"Reduces magic defence by 1 stage until the end of the next round."
        self.name = "Thunderstruck"
        self.icon = ':part_alternation_mark:'
        self.element = Elements.LIGHTNING
        self.category = Category.MAGIC
        self.can_add_instances = True

    @property
    def turn_duration(self) -> int:
        return -1

    @property
    def round_duration(self):
        return 2

    @property
    def application_recap(self) -> str:
        return f"{self.target.nickname}'s magic defence fell."

    def apply_stat_changes(self) -> None:
        self._update_m_def_stages(-1)
