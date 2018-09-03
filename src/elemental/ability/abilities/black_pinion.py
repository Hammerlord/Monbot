from src.core.elements import Elements, Category
from src.elemental.ability.ability import Ability, Target


class BlackPinion(Ability):

    def __init__(self):
        super().__init__()
        self.name = "Black Pinion"
        self._description = "Strike the opponent with a flurry of shadows."
        self.element = Elements.DARK
        self.category = Category.MAGIC
        self.attack_power = 13
        self.mana_cost = 7
        self.defend_cost = 0
        self.targeting = Target.ENEMY
