from src.core.elements import Elements, Category
from src.elemental.ability.ability import Ability, Target, TurnPriority
from src.elemental.status_effect.status_effects.blessed_rain import BlessedRainEffect


class BlessedRain(Ability):
    def __init__(self):
        super().__init__()
        self.name = "Blessed Rain"
        self._description = ("Heals your active elemental for 15% of the "
                             f"caster's health every turn for {self.status_effect.turn_duration} turns.")
        self.icon = ':cloud_rain:'
        self.element = Elements.WATER
        self.category = Category.MAGIC
        self.mana_cost = 15
        self.turn_priority = TurnPriority.NORMAL
        self.targeting = Target.SELF_TEAM

    @property
    def status_effect(self) -> BlessedRainEffect:
        return BlessedRainEffect()
