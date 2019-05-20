from enum import Enum


class ItemTypes(Enum):
    CONSUMABLE = 0
    MATERIAL = 1
    SHARD = 2


class Item:
    item_type: ItemTypes
    name: str
    description: str

    # Item icons are used as reactions, and must be unicode or custom. See Discord add_reaction().
    icon: str

    buy_price: int or None
    sell_price: int or None

    @staticmethod
    def is_usable_on(target):
        return False

    @staticmethod
    def use_on(target):
        pass
