from typing import List

from src.core.elements import Elements
from src.elemental.ability.ability import Ability, LearnableAbility


class AbilityOptionView:
    """
    Represents a single ability as a menu option.
    """
    def __init__(self, ability: Ability or LearnableAbility):
        self.ability = ability

    @staticmethod
    def names_from_list(abilities: List[Ability] or List[LearnableAbility]) -> str:
        """
        :return: A string view for displaying multiple Ability icons and names.
        """
        return '   '.join([AbilityOptionView(ability).get_name() for ability in abilities])

    @staticmethod
    def detail_from_list(abilities: List[Ability] or List[LearnableAbility]) -> str:
        """
        :return: A string view for displaying multiple Abilities and their descriptions.
        """
        return '\n'.join([AbilityOptionView(ability).get_detail() for ability in abilities])

    @staticmethod
    def summary_from_list(abilities: List[Ability] or List[LearnableAbility]) -> str:
        """
        :return: A string view for displaying multiple Ability summaries.
        """
        return '\n'.join([AbilityOptionView(ability).get_summary() for ability in abilities])

    def get_name(self) -> str:
        ability = self.ability
        return f"{ability.icon} {ability.name}"

    def get_summary(self) -> str:
        """
        :return: String representation of the ability, without the description.
        """
        ability = self.ability
        icon = Elements.get_icon(ability.element)
        return (f"{ability.icon} {ability.name} [{ability.category.name}{icon}] "
                f"[{self._get_mana_cost()}:small_blue_diamond:]{self._get_power(ability)}")

    def get_detail(self) -> str:
        ability = self.ability
        return '\n'.join([self.get_summary(), ability.description])

    def _get_mana_cost(self) -> str:
        mana_cost = self.ability.mana_cost
        if mana_cost > 0:
            return f"Cost: {mana_cost}"
        if mana_cost < 0:
            return f"+{mana_cost}"
        return "0"

    @staticmethod
    def _get_power(ability: Ability or LearnableAbility) -> str:
        if ability.base_power > 0:
            return f' - Power: {ability.base_power}'
        return ''
