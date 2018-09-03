from src.core.elements import Elements, Category
from src.elemental.ability.ability import Target, Ability


class Counter(Ability):

    def __init__(self):
        super().__init__()
        self.name = "Counter"
        self._description = "+75% damage if the user blocked damage last turn."
        self.element = Elements.EARTH
        self.category = Category.PHYSICAL
        self.attack_power = 10
        self.mana_cost = 6
        self.targeting = Target.ENEMY

    @staticmethod
    def get_bonus_multiplier(target, actor) -> float:
        if actor.actions and actor.actions[-1].damage_blocked > 0:
            return 1.75
        return 1
