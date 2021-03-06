from src.core.elements import Elements, Category
from src.elemental.ability.ability import Ability


class Rampage(Ability):
    def __init__(self):
        super().__init__()
        self.name = 'Rampage'
        self._description = ("Strike the opponent in a fury over the next 3 turns. "
                             "During this time, no other action can be taken.")
        self.element = Elements.EARTH
        self.mana_cost = 8
        self.attack_power = 12
        self.category = Category.PHYSICAL

    @property
    def base_channel_time(self) -> int:
        return 3

    def get_recap(self, elemental_name: str) -> str:
        return f"{elemental_name} has entered a rampage!"
