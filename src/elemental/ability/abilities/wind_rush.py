from src.core.elements import Elements, Category
from src.elemental.ability.ability import Ability, Target, TurnPriority
from src.elemental.status_effect.status_effects.wind_rush import WindrushEffect


class Windrush(Ability):
    def __init__(self):
        super().__init__()
        self.name = "Windrush"
        self._description = ("Increases mana gained by your active elemental by "
                             f"2 per turn for {self.status_effect.turn_duration} turns.")
        self.icon = ':wind_blowing_face:'
        self.element = Elements.WIND
        self.category = Category.MAGIC
        self.mana_cost = 4
        self.turn_priority = TurnPriority.NORMAL
        self.targeting = Target.SELF_TEAM

    @property
    def status_effect(self) -> WindrushEffect:
        return WindrushEffect()
