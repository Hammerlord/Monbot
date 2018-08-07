from src.character.inventory import Item, ItemTypes
from src.core.constants import PEACH, HAMMER, MANA_SHARD, CAKE, PUDDING, MEAT


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
        self.sell_price = 5


class Cake(Item):
    def __init__(self):
        super().__init__()
        self.name = 'Slice of Cake'
        self.description = 'A delicious frosted cake topped with a strawberry.'
        self.icon = CAKE
        self.exp = 15
        self.healing_percentage = 0.5
        self.sell_price = 5


class Meat(Item):
    def __init__(self):
        super().__init__()
        self.name = 'Meat on Bone'
        self.description = 'Succulent meat on a bone. Makes a hearty meal.'
        self.icon = MEAT
        self.exp = 20
        self.healing_percentage = 0.7
        self.sell_price = 8


class Pudding(Item):
    def __init__(self):
        super().__init__()
        self.name = 'Pudding'
        self.description = 'A mango pudding with a chocolate top.'
        self.icon = PUDDING
        self.exp = 100
        self.healing_percentage = 0.2
        self.sell_price = 15
