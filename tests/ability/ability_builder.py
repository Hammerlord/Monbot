from src.core.elements import Elements, Category
from src.elemental.ability.ability import Ability, TurnPriority


class AbilityBuilder:
    """
    Customize a test Ability.
    """
    def __init__(self):
        self.mana_cost = 0
        self.defend_cost = 0
        self.turn_priority = TurnPriority.NORMAL
        self.element = Elements.NONE
        self.category = Category.NONE  # Eg. magic or physical.
        self.attack_power = 0  # Ie. a damage stat.
        self.recovery = 0  # Ie. a healing stat.
        self.bonus_multiplier = 1

    def with_mana_cost(self, amount: int) -> 'AbilityBuilder':
        self.mana_cost = amount
        return self

    def with_defend_cost(self, amount: int) -> 'AbilityBuilder':
        self.defend_cost = amount
        return self

    def with_turn_priority(self, turn_priority: TurnPriority) -> 'AbilityBuilder':
        self.turn_priority = turn_priority
        return self

    def with_element(self, element: Elements) -> 'AbilityBuilder':
        self.element = element
        return self

    def with_category(self, category: Category) -> 'AbilityBuilder':
        self.category = category
        return self

    def with_attack_power(self, attack_power: int) -> 'AbilityBuilder':
        self.attack_power = attack_power
        return self

    def with_base_recovery(self, recovery: float) -> 'AbilityBuilder':
        self.recovery = recovery
        return self

    def with_bonus_multiplier(self, multiplier: float) -> 'AbilityBuilder':
        self.bonus_multiplier = multiplier
        return self

    def build(self) -> Ability:
        ability = Ability()
        ability.mana_cost = self.mana_cost
        ability.defend_cost = self.defend_cost
        ability.turn_priority = self.turn_priority
        ability.element = self.element
        ability.category = self.category
        ability.attack_power = self.attack_power
        ability.recovery = self.recovery
        ability.bonus_multiplier = self.bonus_multiplier
        return ability
