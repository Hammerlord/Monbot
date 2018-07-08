import discord
from discord.ext.commands import Bot


from src.character.player import Player
from src.ui.forms.battle import BattleView, BattleViewOptions
from src.ui.forms.form import Form, FormOptions
from src.ui.forms.select_starter import SelectStarterView
from src.ui.forms.status import StatusView


class ViewCommandManager:
    """
    Routes user commands to the appropriate view.
    """
    def __init__(self, bot: Bot):
        self.bot = bot
        self.players = {}  # TODO an actual persistence layer

    async def show_status(self, user) -> None:
        self._check_create_profile(user)
        player = self.get_player(user)
        options = FormOptions(self.bot, player)
        if player.num_elementals == 0:
            await self._set_view(player, SelectStarterView(options))
        else:
            await self._set_view(player, StatusView(options))

    async def player_has_starter(self, user) -> bool:
        self._check_create_profile(user)
        player = self.get_player(user)
        options = FormOptions(self.bot, player)
        if player.num_elementals == 0:
            await self._set_view(player, SelectStarterView(options))
            return False
        return True

    async def show_battle(self, player, combat, combat_team) -> None:
        view_options = BattleViewOptions(self.bot,
                                         player,
                                         combat,
                                         combat_team)
        await self._set_view(player, BattleView(view_options))

    def get_view(self, user) -> Form or None:
        player = self.get_player(user)
        if player:
            return player.primary_view

    def get_player(self, user) -> Player or None:
        if user.id in self.players:
            return self.players[user.id]

    async def delete_message(self, message: discord.Message) -> None:
        try:
            await self.bot.delete_message(message)
        except:
            # No permission, or the message was already deleted. Oh well.
            pass

    def _check_create_profile(self, user) -> None:
        # TODO an actual persistence layer
        if user.id not in self.players:
            new_player = Player(user)
            self.players[user.id] = new_player

    async def _set_view(self, player: Player, form: Form) -> None:
        if player.primary_view:
            # Reduce chat clutter by displaying one view message at a time.
            old_message = player.view_message
            await self.delete_message(old_message)
        player.set_primary_view(form)
        await form.render()
