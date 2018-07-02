from src.core.elements import Elements, Category
from src.elemental.ability.ability import Ability, Target


class Slam(Ability):

    """
    A non-elemental physical attack.
    """

    def __init__(self):
        super().__init__()
        self.name = "Slam"
        self._description = "Slam the opponent."
        self.element = Elements.NONE
        self.category = Category.PHYSICAL
        self.base_power = 15
        self.mana_cost = 2
        self.defend_cost = 0
        self.targeting = Target.ENEMY
