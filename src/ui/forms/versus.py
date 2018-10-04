from typing import List

import asyncio
import discord
from discord.ext.commands import Bot

from src.character.player import Player
from src.combat.battle_manager import BattleManager
from src.core.constants import FIGHT, CANCEL
from src.data.data_manager import DataManager
from src.team.team import Team
from src.ui.forms.battle import BattleViewOptions, BattleView
from src.ui.forms.form import ValueForm, FormOptions, Form


class VersusFormOptions(FormOptions):
    def __init__(self,
                 bot: Bot,
                 player,
                 data_manager: DataManager,
                 server,
                 discord_message: discord.Message = None,
                 previous_form: 'Form' = None):
        super().__init__(bot, player, discord_message, previous_form)
        self.data_manager = data_manager
        self.server = server


class VersusForm(ValueForm):
    """
    A form to challenge a user to PVP and wait for a response.
    """

    def __init__(self, options: VersusFormOptions):
        super().__init__(options)
        self.server = options.server
        self.data_manager = options.data_manager
        self.other_players = self._init_other_players()

    def _init_other_players(self) -> List[Player]:
        players = []
        for user in self.server.members:
            other_player = self.data_manager.get_player(user)
            if self._is_valid_opponent(other_player):
                players.append(other_player)
        return sorted(players)

    @property
    def values(self) -> List[Player]:
        max_options = len(ValueForm.ENUMERATED_REACTIONS)
        return self.other_players[:max_options]

    async def render(self) -> None:
        await self._display(self._view)
        await self._clear_reactions()
        for button in self.buttons:
            await self._add_reaction(button.reaction)

    @property
    def _view(self) -> str:
        if not self.values:
            return f'```There are no other players on {self.server.name}.```'
        view = [f'```Select a player from {self.server.name} to challenge.```']
        for button in self.buttons:
            player = button.value
            view.append(f"{button.reaction} {player.nickname} - [Elementals: {player.team.size}/{Team.MAX_SIZE}] "
                        f"Average level: {player.team.average_elemental_level}")
        return '\n'.join(view)

    @property
    def buttons(self) -> List[ValueForm.Button]:
        return self.enumerated_buttons(self.values)

    def _is_valid_opponent(self, opponent: Player) -> bool:
        return (opponent is not None and
                opponent.can_battle and
                opponent is not self.player)

    async def pick_option(self, reaction: str) -> None:
        await super().pick_option(reaction)
        opponent = self._selected_value
        if opponent.can_battle:
            # Check because the opponent may no longer be valid.
            options = ChallengeFormOptions(
                self.bot,
                self.player,
                opponent,
                self.discord_message.channel
            )
            challenge_form = ChallengeForm(options)
            await challenge_form.render()
            await challenge_form.start_countdown()
            await self.bot.delete_message(self.discord_message)


class ChallengeFormOptions(FormOptions):
    def __init__(self,
                 bot: Bot,
                 player: Player,
                 opponent: Player,
                 channel):
        super().__init__(bot, player)
        self.opponent = opponent
        self.channel = channel


class ChallengeForm(Form):
    """
    A special form that is persisted in view_manager, as opposed
    to the Player.primary_view. Only the parties involved
    in this challenge can interact with this form.
    """

    def __init__(self, options: ChallengeFormOptions):
        super().__init__(options)
        self.opponent = options.opponent
        self.channel = options.channel
        self.timer = 60  # Users have 1 minute to accept the challenge.
        self.is_waiting_to_start = True

    async def render(self) -> None:
        self.discord_message = await self.bot.send_message(self.channel, self._view)
        self.player.add_challenge(self)
        self.opponent.add_challenge(self)
        await self._add_reactions([FIGHT, CANCEL])

    async def start_countdown(self) -> None:
        while self.is_waiting_to_start:
            if self.timer == 0:
                await self._expire_challenge()
                break
            await asyncio.sleep(1.0)
            self.timer -= 1

    def cancel(self) -> None:
        self.is_waiting_to_start = False
        self.player.remove_challenge(self)
        self.opponent.remove_challenge(self)

    async def validate_option(self, player: Player, reaction: str) -> None:
        if reaction == CANCEL and (player == self.player or player == self.opponent):
            self.cancel()
            await self._render_cancel(player)
        elif reaction == FIGHT and player == self.opponent:
            await self._render_accepted()
            await self._begin_combat()

    @property
    def _view(self) -> str:
        player = self.player
        opponent = self.opponent
        return (f"{player.nickname} has invited <@{opponent.id}> to duel!\n"
                f"```{player.nickname}'s team: [Elementals: {player.team.size}/{Team.MAX_SIZE}] "
                f"Average level: {player.team.average_elemental_level}\n"
                f"--- vs ---\n"
                f"{opponent.nickname}'s team:  [Elementals: {opponent.team.size}/{Team.MAX_SIZE}] "
                f"Average level: {opponent.team.average_elemental_level}``` \n"
                f"Click {FIGHT} to accept, or {CANCEL} to cancel.")

    async def _begin_combat(self) -> None:
        if not self.is_waiting_to_start:
            return
        self.is_waiting_to_start = False
        BattleManager.create_duel(self.player, self.opponent)
        await self._show_fight_start(self.player)
        await self._show_fight_start(self.opponent)

    async def _show_fight_start(self, player: Player) -> None:
        server = self.channel.server
        user = server.get_member(player.id)
        discord_message = await self.bot.send_message(user, f"```Fight vs {self.opponent.nickname} starting!```")
        options = BattleViewOptions(
            self.bot,
            player,
            player.combat_team,
            discord_message
        )
        battle_form = BattleView(options)
        player.set_primary_view(battle_form)
        await battle_form.render()

    async def _render_cancel(self, player: Player) -> None:
        await self._clear_reactions()
        await self._display(f"```{player.nickname} canceled the challenge.```")

    async def _expire_challenge(self) -> None:
        self.cancel()
        await self._clear_reactions()
        await self._display(f"```The challenge from {self.player.nickname} "
                            f"to {self.opponent.nickname} has expired.```")

    async def _render_accepted(self) -> None:
        await self._clear_reactions()
        await self._display(f"```Challenge accepted between "
                            f"{self.player.nickname} and {self.opponent.nickname}!\n"
                            f"Direct messages will be sent shortly.```")

    async def pick_option(self, reaction: str) -> bool:
        # We need to validate who is adding a reaction to this Form. No operation.
        pass
