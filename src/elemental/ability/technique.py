from src.core.elements import Elements, Category


class Technique:
    """
    An interface of properties shared between Abilities and StatusEffects.
    They have something in common, but I don't know what to call it.
    """
    def __init__(self):
        self.name = None  # Str. TBD by descendants
        self.description = None  # Str. TBD by descendants
        self.id = 0  # Int. TBD by descendants
        self.element = Elements.NONE
        self.category = Category.NONE  # Eg. magic or physical.
        self.base_power = 0  # Ie. a damage stat.
        self.base_recovery = 0  # Ie. a healing stat.
        self.bonus_multiplier = 1

    @staticmethod
    def is_multiplier_triggered(target, actor) -> bool:
        """
        Eg., under certain conditions, the technique can do bonus damage, healing, etc.
        Override this method to define conditions, and self.bonus_multiplier to define amount.
        :param target: The CombatElemental receiving the ability or status effect
        :param actor: The CombatElemental using this ability or status effect
        """
        return False