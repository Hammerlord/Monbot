from src.core.constants import PROVOKE
from src.core.elements import Elements, Category
from src.elemental.ability.ability import Ability, TurnPriority, Target
from src.elemental.status_effect.status_effects.burns import IgniteEffect
from src.elemental.status_effect.status_effects.provoke import ProvokeEffect


class Provoke(Ability):
    def __init__(self):
        super().__init__()
        self.name = "Provoke"
        self._description = (f"For 5 turns or until the user leaves the battlefield, "
                             f"the opponent's physical defence is reduced and it cannot switch out.")
        self.icon = PROVOKE
        self.element = Elements.NONE
        self.category = Category.PHYSICAL
        self.mana_cost = 5
        self.turn_priority = TurnPriority.NORMAL
        self.targeting = Target.ENEMY

    @property
    def status_effect(self) -> ProvokeEffect:
        return ProvokeEffect()
