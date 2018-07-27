from src.core.elements import Elements, Category
from src.elemental.ability.ability import Ability, Target


class Reap(Ability):
    def __init__(self):
        super().__init__()
        self.name = "Reap"
        self._description = "Damage increased by 25% for each debuff on the enemy, up to 4."
        self.element = Elements.DARK
        self.category = Category.PHYSICAL
        self.attack_power = 10
        self.mana_cost = 0
        self.defend_cost = 0
        self.targeting = Target.ENEMY

    @staticmethod
    def get_bonus_multiplier(target, actor) -> float:
        return 1 + (target.num_debuffs * 0.25)
