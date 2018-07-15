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

    def on_receive_damage(self, amount: int, actor) -> str:
        """
        :param amount: The amount of damage taken.
        :param actor: The CombatElemental attacking the owner of this buff.
        :return: Str recap of this effect.
        """
        return f"{self.target.nickname} is defending!"

    def apply_stat_changes(self) -> None:
        self.target.update_damage_reduction(self.target.defend_potency)
