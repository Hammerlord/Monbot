from src.core.elements import Elements, Category
from src.elemental.ability.ability import Target, Ability


class Claw(Ability):

    """
    A non-elemental physical attack.
    """

    def __init__(self):
        super().__init__()
        self.name = "Claw"
        self.element = Elements.NONE
        self.category = Category.PHYSICAL
        self.attack_power = 5
        self.mana_cost = -2
        self.defend_cost = 0
        self.targeting = Target.ENEMY
