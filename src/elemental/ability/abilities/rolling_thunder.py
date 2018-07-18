from src.core.elements import Elements, Category
from src.elemental.ability.ability import Ability, TurnPriority, Target
from src.elemental.status_effect.status_effects.rolling_thunder import RollingThunderEffect


class RollingThunder(Ability):
    """
    Applies a debuff onto the enemy team. After a turn, it will detonate onto the enemy team's active elemental.
    """
    def __init__(self):
        super().__init__()
        self.name = "Rolling Thunder"
        self._description = f"Gather thunder clouds around the enemy. After 1 turn, they detonate."
        self.element = Elements.LIGHTNING
        self.category = Category.MAGIC
        self.base_power = 0
        self.mana_cost = 15
        self.turn_priority = TurnPriority.NORMAL
        self.targeting = Target.ENEMY_TEAM

    @property
    def status_effect(self) -> RollingThunderEffect:
        return RollingThunderEffect()
