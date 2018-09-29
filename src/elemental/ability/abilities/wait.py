from src.core.constants import TIME
from src.core.elements import Category, Elements
from src.elemental.ability.ability import Ability, Target


class Wait(Ability):
    """
    If there are no available abilities for a CombatElemental, then a skip ability is offered.
    """
    def __init__(self):
        super().__init__()
        self.name = "Wait"
        self._description = "Wait until next turn."
        self.icon = TIME
        self.element = Elements.NONE
        self.category = Category.NONE
        self.targeting = Target.NONE

    def get_recap(self, elemental_name: str) -> str:
        return f"{elemental_name} bides its time."


class Loaf(Ability):
    def __init__(self):
        super().__init__()
        self.name = "Loaf"
        self._description = "Wait until next turn."
        self.icon = TIME
        self.element = Elements.NONE
        self.category = Category.NONE
        self.targeting = Target.NONE

    def get_recap(self, elemental_name: str) -> str:
        return f"{elemental_name} is loafing around."
