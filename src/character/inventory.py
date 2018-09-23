from typing import List

from src.data.resources import ItemResource, InventoryResource
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

    def __init__(self, owner_id=None):
        self._bag = {}  # {item_name: ItemSlot}
        self.id = owner_id

    @property
    def items(self) -> List[ItemSlot]:
        return [item_slot for item_slot in self._bag.values() if item_slot.amount > 0]

    @property
    def consumables(self) -> List[ItemSlot]:
        return [item_slot for item_slot in self._bag.values()
                if item_slot.item_type == ItemTypes.CONSUMABLE and item_slot.amount > 0]

    @property
    def materials(self) -> List[ItemSlot]:
        return [item_slot for item_slot in self._bag.values()
                if item_slot.item_type == ItemTypes.MATERIAL and item_slot.amount > 0]

    def use_item(self, item: 'Item', target: Elemental or CombatElemental) -> bool:
        if self.has_item(item) and item.use_on(target):
            self._bag[item.name].update_amount(-1)
            return True
        return False

    def add_item(self, item: 'Item', amount=1) -> None:
        if self.has_item(item):
            self._bag[item.name].update_amount(amount)
        else:
            self._bag[item.name] = ItemSlot(item, amount)

    def remove_item(self, item: 'Item', amount=1) -> None:
        if self.has_item(item):
            self._bag[item.name].update_amount(-amount)

    def amount_left(self, item: 'Item') -> int:
        if item.name in self._bag:
            return self._bag[item.name].amount
        return 0

    def has_item(self, item: 'Item') -> bool:
        return self.amount_left(item) > 0

    def to_server(self) -> dict:
        return InventoryResource(
            id=self.id,
            items=[ItemResource(item.name, item.amount) for item in self._bag]
        )._asdict()

