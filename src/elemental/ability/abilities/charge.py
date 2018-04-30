from src.core.elements import Elements, Category
from src.elemental.ability.ability import Ability, Target, TurnPriority


class Charge(Ability):
    def __init__(self):
        super().__init__()
        self.name = "Charge"
        self.description = "Charge the opponent before it can attack! " \
                           "+50% damage if the target is at full health."
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
            return 1.5
        return 1
