from src.core.constants import WINDRUSH
from src.core.elements import Category, Elements
from src.elemental.status_effect.status_effect import StatusEffect, EffectType


class WindrushEffect(StatusEffect):

    def __init__(self):
        super().__init__()
        self.icon = WINDRUSH
        self.name = "Windrush"
        self.effect_type = EffectType.STAT_INCREASE
        self.category = Category.MAGIC
        self.element = Elements.WIND
        self._description = (f"Increases mana gained by your active elemental "
                             f"by 2 per turn for {self.turn_duration} turns.")

    def on_turn_start(self):
        self.target.update_mana(2)

    @property
    def application_recap(self) -> str:
        return f'A strong gust picks up around {self.target.nickname}, boosting its mana gain!'

    @property
    def fade_recap(self) -> str:
        return f'Windrush has subsided from {self.target.nickname}.'

    @property
    def turn_duration(self) -> int:
        return 5
