from src.core.elements import Elements, Category
from src.elemental.ability.ability import Target, Ability


class Counter(Ability):

    def __init__(self):
        super().__init__()
        self.name = "Counter"
        self._description = "Deals 300% damage if the user blocked an attack last turn."
        self.element = Elements.EARTH
        self.category = Category.PHYSICAL
        self.attack_power = 15
        self.mana_cost = 10
        self.defend_cost = 0
        self.targeting = Target.ENEMY

    @staticmethod
    def get_bonus_multiplier(target, actor) -> float:
        if actor.actions and actor.actions[-1].damage_blocked > 0:
            return 3
        return 1
