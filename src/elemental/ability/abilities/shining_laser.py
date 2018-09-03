from src.core.constants import WARNING
from src.core.elements import Elements, Category
from src.elemental.ability.ability import Ability


class ShiningLaser(Ability):
    """
    A charge ability that takes one turn to activate.
    """
    def __init__(self):
        super().__init__()
        self.name = 'Shining Laser'
        self.element = Elements.LIGHT
        self.mana_cost = 7
        self.attack_power = 20
        self.category = Category.MAGIC

    @property
    def base_cast_time(self) -> int:
        return 1

    @staticmethod
    def get_casting_message(elemental_name: str) -> str:
        return f"{WARNING} {elemental_name} is shining mightily!!"
