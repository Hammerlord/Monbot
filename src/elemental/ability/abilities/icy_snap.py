from src.core.constants import FROST
from src.core.elements import Elements, Category
from src.elemental.ability.ability import Ability, Target
from src.elemental.status_effect.status_effects.chill import Chill


class IcySnap(Ability):

    def __init__(self):
        super().__init__()
        self.name = "Icy Snap"
        self._description = "Chills the target, and damage increased by 20% if the target is chilled."
        self.element = Elements.WATER
        self.category = Category.PHYSICAL
        self.icon = FROST
        self.attack_power = 15
        self.mana_cost = 15
        self.defend_cost = 0
        self.targeting = Target.ENEMY

    @staticmethod
    def get_bonus_multiplier(target, actor) -> float:
        if target.is_chilled:
            return 1.2
        return 1

    @property
    def status_effect(self) -> Chill:
        return Chill()
