from src.core.elements import Elements, Category
from src.elemental.ability.ability import Ability, Target, TurnPriority


class Charge(Ability):
    def __init__(self):
        super().__init__()
        self.name = "Charge"
        self._description = "Attack first. +75% damage on a full HP target."
        self.element = Elements.NONE
        self.category = Category.PHYSICAL
        self.attack_power = 10
        self.mana_cost = 5
        self.turn_priority = TurnPriority.HIGH
        self.targeting = Target.ENEMY

    @staticmethod
    def get_bonus_multiplier(target, actor) -> float:
        if target.current_hp == target.max_hp:
            return 1.75
        return 1
