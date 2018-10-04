
from src.core.constants import MANA_SHARD, EARTH_SHARD, LIGHTNING, FIRE, WATER, WIND
from src.items.item import Item, ItemTypes, ItemSubcategories


class Shard(Item):
    def __init__(self):
        super().__init__()
        self.subcategory = ItemSubcategories.NONE
        self.item_type = ItemTypes.MATERIAL
        self.sell_price = None


class ManaShard(Shard):
    def __init__(self):
        super().__init__()
        self.name = 'Mana Shard'
        self.description = 'A crystal of pure mana. It pulses with a faint light.'
        self.icon = MANA_SHARD


class EarthShard(Shard):
    def __init__(self):
        super().__init__()
        self.name = 'Earth Shard'
        self.description = "A crystal infused with earthen mana. Weighty."
        self.icon = EARTH_SHARD


class LightningShard(Shard):
    def __init__(self):
        super().__init__()
        self.name = 'Lightning Shard'
        self.description = "A crystal sparking with lightning mana. It hums softly with an electrical current."
        self.icon = LIGHTNING


class FireShard(Shard):
    def __init__(self):
        super().__init__()
        self.name = 'Fire Shard'
        self.description = "A crystal glowing orange at its core. Warm to the touch."
        self.icon = FIRE


class WaterShard(Shard):
    def __init__(self):
        super().__init__()
        self.name = 'Water Shard'
        self.description = "A radiant blue crystal."
        self.icon = WATER


class WindShard(Shard):
    def __init__(self):
        super().__init__()
        self.name = 'Wind Shard'
        self.description = "A colourless crystal. A light breeze seems to pick up around it."
        self.icon = WIND