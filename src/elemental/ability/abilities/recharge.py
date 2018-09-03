from src.core.constants import RECHARGE
from src.core.elements import Elements
from src.elemental.ability.ability import Ability, Target


class Recharge(Ability):

    def __init__(self):
        super().__init__()
        self.name = "Recharge"
        self._description = f"Recover 40% health."
        self.icon = RECHARGE
        self.element = Elements.LIGHTNING
        self.targeting = Target.SELF
        self.mana_cost = 5
        self.actor_recovery = 0.4
