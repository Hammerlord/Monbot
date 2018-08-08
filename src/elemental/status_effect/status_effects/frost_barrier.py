from src.elemental.status_effect.status_effect import StatusEffect
from src.elemental.status_effect.status_effects.chill import Chill


class FrostBarrierEffect(StatusEffect):
    def __init__(self):
        super().__init__()
        self.name = "Frost Barrier"
        self.damage_reduction = 0.1
        self._description = (f"Reduces damage taken by {int(self.damage_reduction * 10)}%, "
                             f"and attackers are Chilled.")
        self.icon = "☃"

    @property
    def turn_duration(self):
        return 4

    @property
    def application_recap(self) -> str:
        return f"{self.target.nickname} raises a protective layer of frost!"

    def apply_stat_changes(self):
        self.target.update_damage_reduction(self.damage_reduction)

    def on_receive_ability(self, ability, actor) -> True:
        """
        :param actor: CombatElemental
        """
        actor.add_status_effect(Chill())
        return True
