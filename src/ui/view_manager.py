from discord.ext.commands import Bot

from src.character.player import Player
from src.ui.form import Form
from src.ui.select_starter import SelectStarterView
from src.ui.status import StatusView


class ViewManager:
    """
    Routes user commands to the appropriate view.
    """
    def __init__(self, bot: Bot):
        self.bot = bot
        self.players = {}  # TODO an actual persistence layer

    async def get_status(self, user):
        self._check_create_profile(user)
        player = self.get_player(user)
        if player.num_elementals == 0:
            await self.set_view(player, SelectStarterView(self.bot, player))
        else:
            await self.set_view(player, StatusView(self.bot, player))

    async def set_view(self, player: Player, form: Form) -> None:
        if player.primary_view:
            # Reduce chat clutter by displaying one view message at a time.
            old_message = player.view_message
            await self.bot.delete_message(old_message)
        player.set_primary_view(form)
        await form.render()

    def get_view(self, user) -> Form or None:
        player = self.get_player(user)
        if player:
            return player.primary_view

    def get_player(self, user) -> Player or None:
        if user.id in self.players:
            return self.players[user.id]

    def _check_create_profile(self, user):
        # TODO an actual persistence layer
        if user.id not in self.players:
            new_player = Player(user)
            self.players[user.id] = new_player

    async def get_battle(self, user):
        self._check_create_profile(user)
        player = self.get_player(user)
        if player.num_elementals == 0:
            await self.set_view(player, SelectStarterView(self.bot, player))
