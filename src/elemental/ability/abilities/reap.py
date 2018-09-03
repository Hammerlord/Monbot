from src.core.elements import Elements, Category
from src.elemental.ability.ability import Ability, Target


class Reap(Ability):
    def __init__(self):
        super().__init__()
        self.name = "Reap"
        self._description = "+25% damage for each negative effect on the enemy."
        self.element = Elements.DARK
        self.category = Category.PHYSICAL
        self.attack_power = 6
        self.mana_cost = 0
        self.defend_cost = 0
        self.targeting = Target.ENEMY

    @staticmethod
    def get_bonus_multiplier(target, actor) -> float:
        return 1 + (target.num_debuffs * 0.25)
