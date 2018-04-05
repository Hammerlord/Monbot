from src.core.elements import Elements, Category


class Ability:

    """
    Basic information about an ability.
    """

    def __init__(self):
        self.name = None  # Str. TBD by descendants
        self.id = 0  # Int. TBD by descendants
        self.element = Elements.NONE
        self.category = Category.NONE
        self.base_power = 0
        self.mana_cost = 0
        self.defend_cost = 0
        self.turn_priority = 0

    def execute(self, target: 'CombatElemental'):
        pass

    def targeting(self):
        pass


class LearnableAbility:

    """
    Wraps an Ability with requirements, learnable by a particular Elemental.
    The requirements can be one or more of the following:
    elemental.level -- up to 60
    elemental.ferocity -- up to 3
    elemental.attunement -- same as ferocity, and so on
    elemental.sturdiness
    elemental.resolve
    elemental.resistance
    elemental.swiftness
    """

    def __init__(self, ability: Ability):
        self._ability = ability

    @property
    def ability(self) -> Ability:
        return self._ability

    @staticmethod
    def are_requirements_fulfilled(elemental: 'Elemental') -> bool:
        """
        Override this method to customize the requirements.
        :param elemental: The Elemental trying to learn this ability.
        """
        return elemental.level > 0
