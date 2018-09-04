from src.core.elements import Elements, Category
from src.elemental.ability.ability import Ability, Target
from src.elemental.status_effect.status_effects.stun import Stun


class Aurora(Ability):

    def __init__(self):
        super().__init__()
        self.name = "Aurora"
        self._description = "Stuns opponents for 1 turn."
        self.element = Elements.LIGHT
        self.category = Category.MAGIC
        self.attack_power = 15
        self.mana_cost = 11
        self.defend_cost = 0
        self.targeting = Target.ENEMY_AOE

    @property
    def status_effect(self) -> Stun:
        return Stun()
