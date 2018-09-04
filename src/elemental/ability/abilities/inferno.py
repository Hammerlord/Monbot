from src.core.elements import Elements, Category
from src.elemental.ability.ability import Ability, Target
from src.elemental.status_effect.status_effects.burns import Burn


class Inferno(Ability):

    def __init__(self):
        super().__init__()
        self.name = "Inferno"
        self._description = "Inflicts a burn for 4 turns. +20% damage to burning targets."
        self.element = Elements.FIRE
        self.category = Category.MAGIC
        self.attack_power = 17
        self.mana_cost = 12
        self.defend_cost = 0
        self.targeting = Target.ENEMY_AOE

    @staticmethod
    def get_bonus_multiplier(target, actor) -> float:
        if target.is_burning:
            return 1.2
        return 1

    @property
    def status_effect(self) -> Burn:
        return Burn()
