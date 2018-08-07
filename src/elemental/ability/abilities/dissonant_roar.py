from src.core.elements import Elements, Category
from src.elemental.ability.ability import Ability, Target
from src.elemental.status_effect.status_effects.dissonant_roar import DissonantRoarEffect


class DissonantRoar(Ability):

    def __init__(self):
        super().__init__()
        self.name = "Dissonant Roar"
        self._description = "Unleash an ear-shattering roar, greatly reducing the opponent's magic attack."
        self.element = Elements.DARK
        self.category = Category.MAGIC
        self.attack_power = 0
        self.mana_cost = 10
        self.defend_cost = 0
        self.targeting = Target.ENEMY

    @property
    def status_effect(self) -> DissonantRoarEffect:
        return DissonantRoarEffect()
