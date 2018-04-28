from src.core.elements import Elements, Category
from src.elemental.ability.ability import Target, Ability, AbilityType


class Claw(Ability):

    """
    A non-elemental physical attack.
    """

    def __init__(self):
        super().__init__()
        self.name = "Claw"
        self.description = "Rake the opponent, dealing physical damage."
        self.id = 2
        self.element = Elements.NONE
        self.category = Category.PHYSICAL
        self.base_power = 10
        self.mana_cost = 0
        self.defend_cost = 0
        self.targeting = Target.ENEMY
        self.ability_type = AbilityType.DAMAGE