from src.core.constants import MANA, DEFEND
from src.ui.health_bar import HealthBarView


class Battlefield:
    """
    A string representation of the active elemental(s) on both sides of the field.
    """
    def __init__(self,
                 active_elemental,
                 opponent):
        self.elemental = active_elemental
        self.opponent = opponent

    def get_view(self) -> str:
        elemental = self.elemental
        opponent = self.opponent
        return (f"{opponent.nickname} Lv. {opponent.level}  {self.get_status_effects(opponent)}\n"
                f"`{HealthBarView.from_elemental(opponent)} ({opponent.health_percent}%)`  {opponent.icon}\n"
                f"{elemental.icon}   {elemental.nickname} Lv. {elemental.level}  {self.get_status_effects(elemental)}\n"
                f"         `{HealthBarView.from_elemental(elemental)} ({elemental.current_hp}/{elemental.max_hp})\n`"
                f"{MANA}`{elemental.current_mana}/{elemental.max_mana}`   {DEFEND} `{elemental.defend_charges}`")

    @staticmethod
    def get_status_effects(elemental) -> str:
        return ' '.join([status_effect.icon for status_effect in elemental.status_effects])
