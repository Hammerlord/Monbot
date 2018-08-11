from src.core.elements import Elements, Category
from src.elemental.ability.ability import Target, Ability


class Fireball(Ability):

    """
    A moderate fire attack.
    """

    def __init__(self):
        super().__init__()
        self.name = "Fireball"
        self._description = "Launch a fireball. +30% damage to burning enemies."
        self.element = Elements.FIRE
        self.category = Category.MAGIC
        self.attack_power = 12
        self.mana_cost = 10
        self.defend_cost = 0
        self.targeting = Target.ENEMY

    @staticmethod
    def get_bonus_multiplier(target, actor) -> float:
        if target.is_burning:
            return 1.3
        return 1
