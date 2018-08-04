from src.character.inventory import Item
from src.core.constants import PEACH, HAMMER


class Peach(Item):
    def __init__(self):
        super().__init__()
        self.name = 'Peach'
        self.description = 'A ripe and juicy peach.'
        self.icon = PEACH
        self.healing_percentage = 0.35
        self.exp = 5
        self.sell_price = 1


class Revive(Item):
    def __init__(self):
        super().__init__()
        self.name = 'Revive'
        self.description = 'Revive a knocked-out elemental.'
        self.icon = HAMMER
        self.healing_percentage = 0.15
        self.resurrects_target = True
        self.sell_price = 10
