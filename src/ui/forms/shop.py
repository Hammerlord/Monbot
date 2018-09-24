from typing import List

import discord
from discord.ext.commands import Bot

from src.core.constants import BUY
from src.data.data_manager import DataManager
from src.shop.shop import Shop, ShopItemSlot
from src.ui.forms.form import ValueForm, FormOptions, Form


class ShopViewOptions(FormOptions):
    def __init__(self,
                 bot: Bot,
                 player,
                 shop: Shop,
                 discord_message: discord.Message = None,
                 previous_form: 'Form' = None):
        super().__init__(bot, player, discord_message, previous_form)
        self.shop = shop


class ShopView(ValueForm):
    """
    A form to purchase items from a particular Shop.
    """

    def __init__(self, options: ShopViewOptions):
        super().__init__(options)
        self.shop = options.shop

    @property
    def buttons(self) -> List[ValueForm.Button]:
        return self.ordered_buttons(self.values)

    @property
    def values(self) -> List[ShopItemSlot]:
        return self.shop.inventory

    async def render(self) -> None:
        await self._display(self._view)
        await self._clear_reactions()
        for button in self.buttons:
            await self._add_reaction(button.reaction)

    @property
    def _view(self) -> str:
        view = [f'```{self.shop.name}```']
        for button in self.buttons:
            item_slot = button.value
            view.append(f"{button.reaction}  {item_slot.icon} **{item_slot.name} x{item_slot.quantity}**  "
                        f"{item_slot.properties}   Cost: {item_slot.price} gold")
        view.append(f"```{self._cart}```")
        return '\n'.join(view)

    @property
    def _cart(self) -> str:
        if not self._selected_values:
            return f"{self.player.nickname}'s gold: {self.player.gold}"
        cart_items = ', '.join([f"{item.name} x{item.quantity}" for item in self._selected_values])
        view = [f"Selected: {cart_items}",
                f"Total cost: {self._total_cost} gold",
                f"{self.player.nickname}'s gold: {self.player.gold}"]
        if not self._can_checkout:
            view.append("You don't have enough money for this transaction.")
        return '\n'.join(view)

    @property
    def _total_cost(self) -> int:
        """
        :return: The total price of the items in cart.
        """
        if self._selected_values:
            return sum([item.price for item in self._selected_values])
        return 0

    @property
    def _can_checkout(self) -> bool:
        return self.player.gold >= self._total_cost

    async def _finish_purchase(self) -> None:
        for selected_item in self._selected_values:
            self.shop.buy(selected_item, self.player)
        self.toggled = []
        data_manager = DataManager()
        data_manager.update_player(self.player)
        data_manager.update_inventory(self.player)
        await self.render()

    async def pick_option(self, reaction: str):
        await super().pick_option(reaction)
        if self._selected_value:
            await self._add_reaction(BUY)
        if reaction == BUY and self._selected_value and self._can_checkout:
            await self._finish_purchase()
        await self._display(self._view)

    async def remove_option(self, reaction: str):
        await super().remove_option(reaction)
        await self._display(self._view)
