from typing import List

from src.data.resources import ItemResource
from src.elemental.combat_elemental import CombatElemental
from src.elemental.elemental import Elemental
from src.items.item import ItemTypes, Item


class ItemSlot:
    """
    How an Item occupies a space in Inventory.
    """

    def __init__(self, item: 'Item', amount: int):
        self.item = item
        self.amount = amount

    def update_amount(self, amount: int) -> None:
        self.amount += amount

    @property
    def item_type(self) -> 'ItemTypes':
        return self.item.item_type

    @property
    def name(self) -> str:
        return self.item.name

    @property
    def icon(self) -> str:
        return self.item.icon


class Inventory:
    def __init__(self):
        self._bag = {}  # {item_name: ItemSlot}

    @property
    def items(self) -> List[ItemSlot]:
        return [item_slot for item_slot in self._bag.values() if item_slot.amount > 0]

    @property
    def consumables(self) -> List[ItemSlot]:
        return self._filter_item_by_type(ItemTypes.CONSUMABLE)

    @property
    def materials(self) -> List[ItemSlot]:
        return self._filter_item_by_type(ItemTypes.MATERIAL)

    @property
    def shards(self) -> List[ItemSlot]:
        return self._filter_item_by_type(ItemTypes.SHARD)

    def use_item(self, item: 'Item', target: Elemental or CombatElemental) -> bool:
        if self.has_item(item) and item.is_usable_on(target):
            item.use_on(target)
            self.remove_item(item)
            return True
        return False

    def add_item(self, item: 'Item', amount=1) -> None:
        if item.name in self._bag:
            self._bag[item.name].update_amount(amount)
        else:
            self._bag[item.name] = ItemSlot(item, amount)

    def remove_item(self, item: 'Item', amount=1) -> None:
        if self.has_item(item, amount):
            self._bag[item.name].update_amount(-amount)

    def amount_left(self, item: 'Item') -> int:
        if item.name in self._bag:
            return self._bag[item.name].amount
        return 0

    def has_item(self, item: 'Item', amount=1) -> bool:
        return self.amount_left(item) >= amount

    def to_server(self) -> List[dict]:
        return [ItemResource(item.name, item.amount)._asdict() for item in self._bag.values()]

    def _filter_item_by_type(self, item_type: ItemTypes) -> List[ItemSlot]:
        return [item_slot for item_slot in self._bag.values()
                if item_slot.item_type == item_type and item_slot.amount > 0]
