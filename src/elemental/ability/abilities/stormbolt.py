from src.core.constants import STORMBOLT
from src.core.elements import Elements, Category
from src.elemental.ability.ability import Ability, Target
from src.elemental.status_effect.status_effects.thunderstruck import Thunderstruck


class Stormbolt(Ability):
    def __init__(self):
        super().__init__()
        self.name = "Stormbolt"
        self._description = "Reduce the opponent's magic defence until the end of the next round."
        self.element = Elements.LIGHTNING
        self.category = Category.MAGIC
        self.icon = STORMBOLT
        self.attack_power = 10
        self.mana_cost = 6
        self.defend_cost = 0
        self.targeting = Target.ENEMY

    @property
    def status_effect(self) -> Thunderstruck:
        return Thunderstruck()
