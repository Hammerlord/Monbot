from src.character.consumables import Peach, Revive, Meat
from src.shop.shop import Shop, ShopItemSlot


class GeneralShop(Shop):
    def __init__(self):
        super().__init__()
        self.inventory = [
            ShopItemSlot(Peach(), price=3),
            ShopItemSlot(Peach(), price=3, quantity=3),
            ShopItemSlot(Meat(), price=15),
            ShopItemSlot(Revive(), price=10),
            ShopItemSlot(Revive(), price=10, quantity=3),
        ]
        self.name = "General Shop"
