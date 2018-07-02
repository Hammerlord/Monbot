from discord.ext.commands import Bot

from src.character.player import Player
from src.ui.form import Form, Status
from src.ui.select_starter import SelectStarter


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
            await self.set_view(player, SelectStarter(self.bot, player))
        else:
            await self.set_view(player, Status(self.bot, player))
        await player.current_view.render()

    async def set_view(self, player: Player, form: Form) -> None:
        if player.current_view:
            # Reduce chat clutter by displaying one view message at a time.
            old_message = player.current_view.message
            player.current_view = None
            await self.bot.delete_message(old_message)
        player.current_view = form

    def get_view(self, user) -> Form or None:
        player = self.get_player(user)
        if not player:
            return None
        return player.current_view

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
            await self.set_view(player, SelectStarter(self.bot))
