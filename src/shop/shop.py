from src.character.character import Character
from src.character.inventory import Item, ItemTypes


class ShopItemSlot:
    """
    How an Item occupies a space in a Shop.
    Maybe there'll be rotating shop items in the future.
    """

    def __init__(self, item: 'Item', price: int, quantity=1):
        self.item = item
        self.price = price*quantity
        self.quantity = quantity

    @property
    def item_type(self) -> 'ItemTypes':
        return self.item.item_type

    @property
    def name(self) -> str:
        return self.item.name

    @property
    def icon(self) -> str:
        return self.item.icon

    @property
    def properties(self) -> str:
        return self.item.properties


class Shop:
    def __init__(self):
        self.inventory = []  # List[ShopItemSlot]
        self.name = "Shop"

    def buy(self, shop_item: ShopItemSlot, character: Character) -> bool:
        """
        :return: True if the item could be purchased by the character.
        """
        if shop_item not in self.inventory:
            return False
        if character.gold < shop_item.price:
            return False
        item = shop_item.item
        character.add_item(item, shop_item.quantity)
        character.update_gold(-shop_item.price)
        return True

    @staticmethod
    def sell(item: Item, character: Character) -> bool:
        """
        :return: True if the item could be sold.
        """
        if item.sell_price > 0:
            character.remove_item(item)
            character.update_gold(item.sell_price)
            return True
