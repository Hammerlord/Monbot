from src.core.elements import Elements, Category
from src.elemental.ability.ability import Ability, Target
from src.elemental.status_effect.status_effects.quake import QuakeEffect


class Quake(Ability):

    def __init__(self):
        super().__init__()
        self.name = "Quake"
        self._description = "Quake the earth, reducing enemy speed by 1 stage for 3 turns."
        self.element = Elements.EARTH
        self.category = Category.MAGIC
        self.attack_power = 13
        self.mana_cost = 7
        self.defend_cost = 0
        self.targeting = Target.ENEMY

    @property
    def status_effect(self) -> QuakeEffect:
        return QuakeEffect()
