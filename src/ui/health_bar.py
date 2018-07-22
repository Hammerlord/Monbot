import math

from src.elemental.combat_elemental import CombatElemental, CombatElementalLog
from src.elemental.elemental import Elemental


class HealthBarView:

    @staticmethod
    def from_elemental(elemental: Elemental or CombatElemental or CombatElementalLog) -> str:
        return HealthBarView().get_view(elemental.current_hp, elemental.max_hp)

    def get_view(self, current_hp: int, max_hp: int) -> str:
        """
        eg. 83/100 -> ■■■■■■■■◩⧄
        (Ignoring the weird render in this file)
        """
        total_bars = 10
        value = self._get_rounded((current_hp / max_hp) * total_bars)
        num_filled = int(math.floor(value))
        num_empty = total_bars - int(math.ceil(value))
        num_half = total_bars - num_empty - num_filled
        return '■' * num_filled + '◩' * num_half + '⧄' * num_empty

    @staticmethod
    def _get_rounded(value: float) -> float:
        """
        :return: Rounded to the nearest 0.5.
        """
        return round(value * 2) / 2
