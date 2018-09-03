from src.core.constants import SHELL
from src.elemental.ability.ability import Ability, Target
from src.elemental.status_effect.status_effects.stonehide import StonehideEffect


class Stonehide(Ability):

    def __init__(self):
        super().__init__()
        self.name = "Stonehide"
        self._description = f"Reduces damage taken by the next 4 attacks or harmful effects by 30%."
        self.icon = SHELL
        self.targeting = Target.SELF
        self.mana_cost = 4

    @property
    def status_effect(self) -> StonehideEffect:
        return StonehideEffect()
