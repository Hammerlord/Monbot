import discord
from discord.ext.commands import Bot


from src.character.player import Player
from src.shop.shop import Shop
from src.ui.forms.battle import BattleView, BattleViewOptions
from src.ui.forms.form import Form, FormOptions
from src.ui.forms.select_starter import SelectStarterView
from src.ui.forms.shop import ShopViewOptions, ShopView
from src.ui.forms.status import StatusView


class ViewCommandManager:
    """
    Routes user commands to the appropriate view.
    """
    def __init__(self, bot: Bot):
        self.bot = bot

    async def show_starter_selection(self, player: Player) -> None:
        options = FormOptions(self.bot, player)
        await self._set_view(player, SelectStarterView(options))

    async def show_status(self, player: Player) -> None:
        options = FormOptions(self.bot, player)
        await self._set_view(player, StatusView(options))

    async def show_shop(self, shop: Shop, player: Player) -> None:
        options = ShopViewOptions(self.bot, player, shop)
        await self._set_view(player, ShopView(options))

    async def show_battle(self, player, combat, combat_team) -> None:
        view_options = BattleViewOptions(self.bot,
                                         player,
                                         combat,
                                         combat_team)
        await self._set_view(player, BattleView(view_options))

    async def delete_message(self, message: discord.Message) -> None:
        try:
            await self.bot.delete_message(message)
        except:
            # No permission, or the message was already deleted. Oh well.
            pass

    async def _set_view(self, player: Player, form: Form) -> None:
        if player.primary_view:
            # Reduce chat clutter by displaying one view message at a time.
            old_message = player.view_message
            await self.delete_message(old_message)
        player.set_primary_view(form)
        await form.render()
