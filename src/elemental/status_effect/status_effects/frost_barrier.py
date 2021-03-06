from src.core.constants import FROST_BARRIER
from src.elemental.status_effect.status_effect import StatusEffect
from src.elemental.status_effect.status_effects.chill import Chill


class FrostBarrierEffect(StatusEffect):
    def __init__(self):
        super().__init__()
        self.name = "Frost Barrier"
        self._description = (f"Reduces damage taken by {int(self.damage_reduction * 10)}%, "
                             f"and attackers are Chilled.")
        self.icon = FROST_BARRIER

    @property
    def damage_reduction(self) -> float:
        return 0.1

    @property
    def turn_duration(self):
        return 4

    @property
    def application_recap(self) -> str:
        return f"{self.target.nickname} raises a protective layer of frost!"

    def on_receive_ability(self, ability, actor) -> True:
        """
        :param ability: Ability
        :param actor: CombatElemental
        """
        if ability.attack_power > 0:
            actor.add_status_effect(Chill())
            return True
