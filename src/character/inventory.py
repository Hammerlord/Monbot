from collections import namedtuple
from enum import Enum
from typing import List, NamedTuple

from src.core.constants import ITEM
from src.elemental.combat_elemental import CombatElemental
from src.elemental.elemental import Elemental


class ItemSlot:
    def __init__(self, item: 'Item', amount: int):
        self.item = item
        self.amount = amount

    def update_amount(self, amount: int) -> None:
        self.amount += amount


class Inventory:
    def __init__(self):
        self._bag = {}  # {item_name: ItemSlot}

    @property
    def items(self) -> List[ItemSlot]:
        return [item_slot for item_slot in self._bag.values()]

    @property
    def consumables(self) -> List[ItemSlot]:
        return [item_slot for item_slot in self._bag.values() if item_slot.item_type == ItemTypes.CONSUMABLE]

    @property
    def materials(self) -> List[ItemSlot]:
        return [item_slot for item_slot in self._bag.values() if item_slot.item_type == ItemTypes.MATERIAL]

    def use_item(self, item: 'Item', target: Elemental or CombatElemental) -> bool:
        if self._has_item(item) and item.use_on(target):
            self._bag[item.name].update_amount(-1)
            return True
        return False

    def add_item(self, item: 'Item', amount=1) -> None:
        if self._has_item(item):
            self._bag[item.name].update_amount(amount)
        else:
            self._bag[item.name] = ItemSlot(item, amount)

    def amount_left(self, item: 'Item') -> int:
        if self._bag[item.name]:
            return self._bag[item.name].amount
        return 0

    def _has_item(self, item: 'Item') -> bool:
        return item.name in self._bag and self._bag[item.name].amount > 0


class ItemTypes(Enum):
    CONSUMABLE = 0
    MATERIAL = 1


class Item:
    def __init__(self):
        self.healing_percentage = 0
        self.exp = 0
        self.resurrects_target = False
        self.name = 'Meat on a Bone'
        self.description = 'An item.'
        # Item icons are used as reactions, and must be unicode or custom. See Discord add_reaction().
        self.icon = ITEM
        self.item_type = ItemTypes.CONSUMABLE
        self.sell_price = 0

    def is_usable_on(self, target: Elemental or CombatElemental) -> bool:
        if self.healing_percentage == 0 and self.exp == 0:
            return False
        if self.resurrects_target:
            return target.is_knocked_out
        return not target.is_knocked_out

    def use_on(self, target: Elemental or CombatElemental) -> bool:
        """
        Use this item on an Elemental/CombatElemental.
        :return bool: True if this item could be used.
        """
        if self.is_usable_on(target):
            heal_amount = target.max_hp * self.healing_percentage
            target.heal(heal_amount)
            target.add_exp(self.exp)
            return True
        return False

    @property
    def properties(self) -> str:
        """
        Shows what this item does specifically.
        """
        properties = []
        if self.resurrects_target:
            properties.append("[Revives KO]")
        if self.healing_percentage > 0:
            properties.append(f"[+{int(self.healing_percentage * 100)}% HP]")
        if self.exp > 0:
            properties.append(f"[+{self.exp} EXP]")
        return ' '.join(properties)
