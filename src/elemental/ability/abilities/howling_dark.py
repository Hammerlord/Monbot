from src.core.elements import Elements, Category
from src.elemental.ability.ability import Ability, Target


class HowlingDark(Ability):

    def __init__(self):
        super().__init__()
        self.name = "Howling Dark"
        self.element = Elements.DARK
        self.category = Category.MAGIC
        self.attack_power = 20
        self.mana_cost = 12
        self.defend_cost = 0
        self.targeting = Target.ENEMY_CLEAVE
