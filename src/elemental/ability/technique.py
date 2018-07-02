from src.core.elements import Elements, Category


class Technique:
    """
    An interface of properties shared between Abilities and StatusEffects.
    They have something in common, but I don't know what to call it.
    """
    def __init__(self):
        self.name = ''  # Str. TBD by descendants
        self._description = ''  # Str. TBD by descendants
        self.element = Elements.NONE
        self.category = Category.NONE  # Eg. magic or physical.
        self.base_power = 0  # Ie. a damage stat.
        self.base_recovery = 0  # Ie. a healing stat.
        self.icon = ''  # A str icon representing this ability.

    @property
    def description(self) -> str:
        return self._description

    def __str__(self) -> str:
        return self.name

    @staticmethod
    def get_bonus_multiplier(target, actor) -> float:
        """
        Eg., under certain conditions, the technique can do bonus damage, healing, etc.
        Override this method to define conditions and amount.
        :param target: The CombatElemental receiving the ability or status effect
        :param actor: The CombatElemental using this ability or status effect
        """
        return 1
