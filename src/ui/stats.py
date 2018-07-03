from src.elemental.elemental import Elemental


class StatsView:
    def __init__(self, elemental: Elemental):
        self.elemental = elemental

    def get_view(self) -> str:
        elemental = self.elemental
        stats = (f"```Physical attack: {elemental.physical_att}\n"
                 f"Magic attack: {elemental.magic_att}\n"
                 f"Physical defence: {elemental.physical_def}\n"
                 f"Magic defence: {elemental.magic_def}\n"
                 f"Speed: {elemental.speed}```")
        defend = (f":shield: charges: {elemental.defend_charges} -"
                  f" Damage reduced: {elemental.defend_potency * 100}%")
        mana = (f":small_blue_diamond: on combat start: {elemental.starting_mana} \n"
                f":small_blue_diamond: per turn: {elemental.mana_per_turn}")
        return '\n'.join([stats, defend, mana])
