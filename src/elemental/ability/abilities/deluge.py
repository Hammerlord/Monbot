from src.core.constants import DELUGE
from src.core.elements import Elements, Category
from src.elemental.ability.ability import Ability, Target


class Deluge(Ability):

    def __init__(self):
        super().__init__()
        self.name = "Deluge"
        self.element = Elements.WATER
        self.category = Category.MAGIC
        self.icon = DELUGE
        self.attack_power = 20
        self.mana_cost = 12
        self.defend_cost = 0
        self.targeting = Target.ENEMY_CLEAVE
