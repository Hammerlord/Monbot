from src.core.constants import DISSONANT_ROAR
from src.core.elements import Elements, Category
from src.elemental.ability.ability import Ability, Target
from src.elemental.status_effect.status_effects.dissonant_roar import DissonantRoarEffect


class DissonantRoar(Ability):

    def __init__(self):
        super().__init__()
        self.name = "Dissonant Roar"
        self._description = (f"Reduce the opponent's magic attack by 2 stages "
                             f"for {self.status_effect.turn_duration} turns.")
        self.element = Elements.DARK
        self.category = Category.MAGIC
        self.icon = DISSONANT_ROAR
        self.attack_power = 0
        self.mana_cost = 5
        self.defend_cost = 0
        self.targeting = Target.ENEMY

    @property
    def status_effect(self) -> DissonantRoarEffect:
        return DissonantRoarEffect()
