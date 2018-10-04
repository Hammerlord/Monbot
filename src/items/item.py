from enum import Enum

from src.core.constants import MEAT
from src.elemental.combat_elemental import CombatElemental
from src.elemental.elemental import Elemental


class ItemTypes(Enum):
    CONSUMABLE = 0
    MATERIAL = 1


class ItemSubcategories(Enum):
    NONE = 0
    SHARD = 1


class Item:
    def __init__(self):
        self.healing_percentage = 0
        self.exp = 0
        self.resurrects_target = False
        self.name = 'Meat on a Bone'
        self.description = 'An item.'
        # Item icons are used as reactions, and must be unicode or custom. See Discord add_reaction().
        self.icon = MEAT
        self.item_type = ItemTypes.CONSUMABLE
        self.subcategory = ItemSubcategories.NONE
        self.sell_price = 0

    @property
    def buy_price(self) -> int:
        if self.sell_price is not None:
            return self.sell_price * 3

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
