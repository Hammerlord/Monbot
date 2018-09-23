import src.items.consumables
import src.items.materials
from src.items.item import Item


class ItemInitializer:
    ALL_ITEMS = {}

    for item in Item.__subclasses__():
        item_instance = item()
        ALL_ITEMS[item_instance.name] = item_instance

    @staticmethod
    def from_name(item_name: str) -> Item or None:
        if item_name in ItemInitializer.ALL_ITEMS:
            return ItemInitializer.ALL_ITEMS[item_name]
