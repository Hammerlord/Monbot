from src.core.elements import Category, Elements
from src.elemental.status_effect.status_effect import StatusEffect, EffectType


class BlessedRainEffect(StatusEffect):

    def __init__(self):
        super().__init__()
        self.icon = ':cloud_rain:'
        self.effect_type = EffectType.NONE
        self.category = Category.MAGIC
        self.element = Elements.WATER
        self.recovery = 0.15
        self._description = (f"Heals for {self.recovery*100}% of the user's max health "
                             f"every turn for {self.turn_duration} turns.")

    def on_turn_end(self) -> True:
        self.target.heal(self.recovery*self.applier.max_hp)

    @property
    def application_recap(self) -> str:
        return f'A gentle rain begins to fall over {self.target.nickname}.'

    @property
    def trigger_recap(self) -> str:
        return f'Rain gently falls over {self.target.nickname}.'

    @property
    def fade_recap(self) -> str:
        return f'Blessed Rain has subsided from {self.target.nickname}.'

    @property
    def turn_duration(self) -> int:
        return 4
