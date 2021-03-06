from src.core.constants import FROST_BARRIER
from src.elemental.ability.ability import Ability, Target
from src.elemental.status_effect.status_effects.frost_barrier import FrostBarrierEffect


class FrostBarrier(Ability):

    def __init__(self):
        super().__init__()
        self.name = "Frost Barrier"
        self._description = (f"Reduce damage taken by 10% and chill attackers "
                             f"for {self.status_effect.turn_duration} turns.")
        self.icon = FROST_BARRIER
        self.targeting = Target.SELF
        self.mana_cost = 4

    @property
    def status_effect(self) -> FrostBarrierEffect:
        return FrostBarrierEffect()
