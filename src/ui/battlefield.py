from typing import List

from src.combat.combat import Combat
from src.core.constants import MANA, DEFEND, PLACEHOLDER, WARNING, TEAM_INDICATOR, TEAM_KO
from src.ui.health_bar import HealthBarView


class Battlefield:
    """
    A string representation of the active elemental(s) on both sides of the field.
    """

    def __init__(self,
                 allies,
                 opponents):
        """
        :param allies: List[CombatElementalLog]
        :param opponents: List[CombatElementalLog]
        """
        self.allies = allies
        self.opponents = opponents

    def get_view(self) -> str:
        return f"{self._opponent_view}\n{self._ally_view}"

    @property
    def _opponent_view(self) -> str:
        opponent = self.opponents[0]  # TODO 1v1 only
        return (f"{self.get_team_indicators(opponent)}  {self._get_team_status_effects(opponent)}\n"
                f"{opponent.nickname} Lv. {opponent.level}  {self._get_status_effects(opponent)}\n"
                f"`{HealthBarView.from_elemental(opponent)} ({opponent.health_percent}%)`  "
                f"{self._get_icon(opponent)} {self._get_casting(opponent)}")

    @property
    def _ally_view(self) -> str:
        elemental = self.allies[0]  # TODO 1v1 only
        return (
            f"{self._get_icon(elemental)}   {elemental.nickname} "
            f"Lv. {elemental.level} {self._get_status_effects(elemental)}\n"
            f"          `{HealthBarView.from_elemental(elemental)} ({elemental.current_hp}/{elemental.max_hp})\n`"
            f"{MANA}`{elemental.current_mana}/{elemental.max_mana}`   {DEFEND} `{elemental.defend_charges}`\n"
            f"{self.get_team_indicators(elemental)}  {self._get_team_status_effects(elemental)}\n")

    @staticmethod
    def get_team_indicators(elemental) -> str:
        """
        Indicators that show the number of elementals on a team and whether they have been knocked out.
        """
        indicators = []
        for elemental_status in elemental.team_status:
            # If the team member is alive, show an alive indicator. If not, show X.
            if elemental_status:
                # Boolean resolves to true
                indicators.append(TEAM_INDICATOR)
            else:
                indicators.append(TEAM_KO)
        return ''.join(indicators)

    @staticmethod
    def _get_status_effects(elemental) -> str:
        return ' '.join([status_effect.icon for status_effect in elemental.status_effects])

    @staticmethod
    def _get_team_status_effects(elemental) -> str:
        if not elemental.team_status_effects:
            return PLACEHOLDER
        return ' '.join([status_effect.icon for status_effect in elemental.team_status_effects])

    @staticmethod
    def _get_icon(elemental) -> str:
        """
        Show a blank emoji if the elemental is dead.
        """
        if elemental.is_knocked_out:
            return PLACEHOLDER
        return elemental.icon

    @staticmethod
    def _get_casting(elemental) -> str:
        if elemental.is_knocked_out or elemental.action_queued is None:
            return ''
        return WARNING
