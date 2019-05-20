import src.items.consumables
import src.items.shards
from src.items.item import Item


class ItemInitializer:
    ALL_ITEMS = {}

    for item in Item.__subclasses__():
        if item.__subclasses__():
            for sub_item in item.__subclasses__():
                sub_item_instance = sub_item()
                ALL_ITEMS[sub_item_instance.name] = sub_item_instance
        else:
            item_instance = item()
            ALL_ITEMS[item_instance.name] = item_instance

    @staticmethod
    def from_name(item_name: str) -> Item or None:
        if item_name in ItemInitializer.ALL_ITEMS:
            return ItemInitializer.ALL_ITEMS[item_name]
