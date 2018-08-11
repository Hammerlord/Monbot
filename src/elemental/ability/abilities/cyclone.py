from src.core.elements import Elements, Category
from src.elemental.ability.ability import Ability, Target


class Cyclone(Ability):
    def __init__(self):
        super().__init__()
        self.name = "Cyclone"
        self._description = (f"Buffet the enemy with high winds. "
                             "Deals 25% more damage for every consecutive use.")
        self.element = Elements.WIND
        self.category = Category.PHYSICAL
        self.attack_power = 9
        self.mana_cost = 12
        self.defend_cost = 0
        self.targeting = Target.ENEMY

    @staticmethod
    def get_bonus_multiplier(target, actor) -> float:
        multiplier = 1
        for action in reversed(actor.actions):
            if hasattr(action, 'ability') and not isinstance(action.ability, Cyclone):
                break
            multiplier += 0.25
        return multiplier
