from src.core.constants import DEFEND
from src.elemental.status_effect.status_effect import StatusEffect


class DefendEffect(StatusEffect):

    def __init__(self):
        super().__init__()
        self.icon = DEFEND

    @property
    def _base_duration(self) -> int:
        """
        :return 0: Lasts until the end of the round.
        """
        return 0

    def on_effect_start(self) -> None:
        # Block damage against any end of turn debuffs as well.
        self.apply_stat_changes()

    def apply_stat_changes(self) -> None:
        self.target.update_damage_reduction(self.target.defend_potency)

    def on_receive_damage(self, amount: int, actor) -> bool:
        return True

    def activation_recap(self) -> str:
        return f'{self.target.nickname} defended the attack!'
