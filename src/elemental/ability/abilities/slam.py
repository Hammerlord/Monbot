from src.core.elements import Elements, Category
from src.elemental.ability.ability import Ability, Target


class Slam(Ability):

    """
    A non-elemental physical attack.
    """

    def __init__(self):
        super().__init__()
        self.name = "Slam"
        self.element = Elements.NONE
        self.category = Category.PHYSICAL
        self.attack_power = 7
        self.mana_cost = -1
        self.defend_cost = 0
        self.targeting = Target.ENEMY
