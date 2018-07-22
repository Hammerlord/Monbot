from src.combat.combat import Combat
from src.core.constants import MANA, DEFEND
from src.ui.health_bar import HealthBarView


class Battlefield:
    """
    A string representation of the active elemental(s) on both sides of the field.
    """
    def __init__(self,
                 side_a,
                 side_b,
                 for_team):
        """
        :param side_a: List[CombatElementalLog]
        :param side_b: List[CombatElementalLog]
        """
        self.allies = side_a if for_team.side == Combat.SIDE_A else side_b
        self.opponents = side_b if self.allies == side_a else side_a

    def get_view(self) -> str:
        # TODO 1v1 only
        elemental = self.allies[0]
        opponent = self.opponents[0]
        return (f"{opponent.nickname} Lv. {opponent.level}  {self.get_status_effects(opponent)}\n"
                f"`{HealthBarView.from_elemental(opponent)} ({opponent.health_percent}%)`  {opponent.icon}\n"
                f"{elemental.icon}   {elemental.nickname} Lv. {elemental.level}  {self.get_status_effects(elemental)}\n"
                f"         `{HealthBarView.from_elemental(elemental)} ({elemental.current_hp}/{elemental.max_hp})\n`"
                f"{MANA}`{elemental.current_mana}/{elemental.max_mana}`   {DEFEND} `{elemental.defend_charges}`")

    @staticmethod
    def get_status_effects(elemental) -> str:
        return ' '.join([status_effect.icon for status_effect in elemental.status_effects])
