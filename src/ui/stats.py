from src.elemental.elemental import Elemental
from src.ui.ability_option import AbilityOptionView


class StatsView:
    def __init__(self, elemental: Elemental):
        self.elemental = elemental

    def get_view(self) -> str:
        elemental = self.elemental
        stats = (f"```Python\n"
                 f"Physical attack: {elemental.physical_att}   Magic attack: {elemental.magic_att}\n"
                 f"Physical defence: {elemental.physical_def}   Magic defence: {elemental.magic_def}\n"
                 f"Speed: {elemental.speed}\n"
                 "\n"
                 f"🛡 charges: {elemental.defend_charges} -"
                 f" Damage reduced: {elemental.defend_potency * 100}%\n"
                 f"🔹 on combat start: {elemental.starting_mana}\n"
                 f"🔹 per turn: {elemental.mana_per_turn}\n"
                 "\n"
                 f"{self.attributes_view}"
                 "```")
        return ''.join([stats, self.abilities_view])

    @property
    def attributes_view(self) -> str:
        attributes = '   '.join([f"[{attribute.name} Lv. {attribute.level}]"
                                 for attribute in self.elemental.attributes])
        points = self.elemental.attribute_points
        return '\n'.join([
            'Attributes' if points == 0 else f'Attributes ({points} points)',
            attributes
        ])

    @property
    def abilities_view(self) -> str:
        return '\n'.join([
            '\nActive abilities',
            AbilityOptionView.names_from_list(self.elemental.active_abilities)
        ])
