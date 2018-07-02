from src.core.elements import Elements, Category
from src.elemental.ability.ability import Ability, Target, TurnPriority


class Charge(Ability):
    def __init__(self):
        super().__init__()
        self.name = "Charge"
        self._description = ("Charge before the opponent can attack! "
                             "2x damage on targets at full health.")
        self.element = Elements.NONE
        self.category = Category.PHYSICAL
        self.base_power = 15
        self.mana_cost = 10
        self.defend_cost = 0
        self.turn_priority = TurnPriority.HIGH
        self.targeting = Target.ENEMY

    @staticmethod
    def get_bonus_multiplier(target, actor) -> float:
        if target.current_hp == target.max_hp:
            return 2
        return 1
