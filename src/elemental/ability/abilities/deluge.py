from src.core.elements import Elements, Category
from src.elemental.ability.ability import Ability, Target


class Deluge(Ability):

    def __init__(self):
        super().__init__()
        self.name = "Deluge"
        self._description = "Unleash the strength of open water."
        self.element = Elements.WATER
        self.category = Category.MAGIC
        self.icon = ":anchor:"
        self.attack_power = 35
        self.mana_cost = 25
        self.defend_cost = 0
        self.targeting = Target.ENEMY_CLEAVE
