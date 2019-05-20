
from src.core.constants import MANA_SHARD, EARTH_SHARD, LIGHTNING, FIRE, WATER, WIND, DARK, LIGHT, CHAOS
from src.core.elements import Elements
from src.items.item import Item, ItemTypes


class Shard(Item):
    item_type = ItemTypes.SHARD
    sell_price = None
    element = Elements.NONE


class ManaShard(Shard):
    name = 'Mana Shard'
    description = 'A crystal of pure mana. It pulses with a faint light.'
    icon = MANA_SHARD


class EarthShard(Shard):
    name = 'Earth Shard'
    description = "A crystal infused with earthen mana. Weighty."
    icon = EARTH_SHARD
    element = Elements.EARTH


class LightningShard(Shard):
    name = 'Lightning Shard'
    description = "A crystal sparking with lightning mana. It hums softly with an electrical current."
    icon = LIGHTNING
    element = Elements.LIGHTNING


class FireShard(Shard):
    name = 'Fire Shard'
    description = "A crystal glowing orange at its core. Warm to the touch."
    icon = FIRE
    element = Elements.FIRE


class WaterShard(Shard):
    name = 'Water Shard'
    description = "A radiant blue crystal."
    icon = WATER
    element = Elements.WATER


class WindShard(Shard):
    name = 'Wind Shard'
    description = "A colourless crystal. A light breeze seems to pick up around it."
    icon = WIND
    element = Elements.WIND


class ShadowShard(Shard):
    name = 'Shadow Shard'
    description = "A shard of pure darkness. No light can pass through it."
    icon = DARK
    element = Elements.DARK


class LightShard(Shard):
    name = 'Light Shard'
    description = "A shard of pure light. It glows like the sun."
    icon = LIGHT
    element = Elements.LIGHT


class ChaosShard(Shard):
    name = 'Chaos Shard'
    description = "A crystal emitting an eerie pallid glow."
    icon = CHAOS
    element = Elements.CHAOS
