from src.core.constants import ROLLING_THUNDER
from src.core.elements import Elements, Category
from src.elemental.ability.ability import Ability, TurnPriority, Target
from src.elemental.status_effect.status_effects.rolling_thunder import RollingThunderEffect


class RollingThunder(Ability):
    """
    Applies a debuff onto the enemy team.
    """
    def __init__(self):
        super().__init__()
        self.name = "Rolling Thunder"
        self._description = (f"Gather thunder clouds over the opponent's team "
                             f"that detonate at the end of the next round.")
        self.element = Elements.LIGHTNING
        self.icon = ROLLING_THUNDER
        self.category = Category.MAGIC
        self.mana_cost = 6
        self.turn_priority = TurnPriority.NORMAL
        self.targeting = Target.ENEMY_TEAM

    @property
    def status_effect(self) -> RollingThunderEffect:
        return RollingThunderEffect()
