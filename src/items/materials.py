
from src.core.constants import MANA_SHARD, EARTH_SHARD, LIGHTNING, FIRE, WATER, WIND, DARK, LIGHT, CHAOS
from src.core.elements import Elements
from src.items.item import Item, ItemTypes, ItemSubcategories


class Shard(Item):
    def __init__(self):
        super().__init__()
        self.subcategory = ItemSubcategories.SHARD
        self.item_type = ItemTypes.MATERIAL
        self.sell_price = None
        self.element = Elements.NONE


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
        self.element = Elements.EARTH


class LightningShard(Shard):
    def __init__(self):
        super().__init__()
        self.name = 'Lightning Shard'
        self.description = "A crystal sparking with lightning mana. It hums softly with an electrical current."
        self.icon = LIGHTNING
        self.element = Elements.LIGHTNING


class FireShard(Shard):
    def __init__(self):
        super().__init__()
        self.name = 'Fire Shard'
        self.description = "A crystal glowing orange at its core. Warm to the touch."
        self.icon = FIRE
        self.element = Elements.FIRE


class WaterShard(Shard):
    def __init__(self):
        super().__init__()
        self.name = 'Water Shard'
        self.description = "A radiant blue crystal."
        self.icon = WATER
        self.element = Elements.WATER


class WindShard(Shard):
    def __init__(self):
        super().__init__()
        self.name = 'Wind Shard'
        self.description = "A colourless crystal. A light breeze seems to pick up around it."
        self.icon = WIND
        self.element = Elements.WIND


class ShadowShard(Shard):
    def __init__(self):
        super().__init__()
        self.name = 'Shadow Shard'
        self.description = "A shard of pure darkness. No light can pass through it."
        self.icon = DARK
        self.element = Elements.DARK


class LightShard(Shard):
    def __init__(self):
        super().__init__()
        self.name = 'Light Shard'
        self.description = "A shard of pure light. It glows like the sun."
        self.icon = LIGHT
        self.element = Elements.LIGHT


class ChaosShard(Shard):
    def __init__(self):
        super().__init__()
        self.name = 'Chaos Shard'
        self.description = "A crystal emitting an eerie pallid glow."
        self.icon = CHAOS
        self.element = Elements.CHAOS
