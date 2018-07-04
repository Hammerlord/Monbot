from typing import List

import discord
from discord.ext.commands import Bot

from src.core.constants import *
from src.elemental.elemental import Elemental
from src.ui.form import Form, FormOptions
from src.ui.health_bar import HealthBarView
from src.ui.stats import StatsView


class StatusView(Form):
    """
    Shows the status of your team.
    """
    def __init__(self, options: FormOptions):
        super().__init__(options)
        self.values: List[Elemental] = self.player.team.elementals
        self.initial_render = True

    @property
    def buttons(self) -> List[Form.Button]:
        return self.enumerated_buttons(self.values)

    async def render(self) -> None:
        if self.discord_message:
            await self.bot.clear_reactions(self.discord_message)
        await self._display(self._get_page())
        for button in self.buttons:
            await self.bot.add_reaction(self.discord_message, button.reaction)

    def _get_page(self) -> str:
        message_body = f"```{self.player.nickname}'s Team (Slots: {self.player.team.size}/4)```"
        for i, elemental in enumerate(self.values):
            message_body += self._get_status(i, elemental)
        return message_body

    @staticmethod
    def _get_status(index: int, elemental: Elemental) -> str:
        return (f"{index + 1}) {elemental.left_icon}  Lv. {elemental.level} {elemental.nickname} "
                f"`{HealthBarView.from_elemental(elemental)} "
                f"{elemental.current_hp} / {elemental.max_hp} HP` \n")

    async def pick_option(self, reaction: str) -> None:
        await super().pick_option(reaction)
        if self._selected_value is not None:
            await self.create_detail_view(self._selected_value)

    async def create_detail_view(self, elemental: Elemental) -> None:
        options = StatusDetailOptions(self.bot, self.player, elemental, self.discord_message)
        form = StatusDetailView(options)
        self.player.set_primary_view(form)
        await form.render()


class StatusDetailOptions(FormOptions):
    def __init__(self,
                 bot: Bot,
                 player,
                 elemental: Elemental,
                 discord_message: discord.Message=None):
        super().__init__(bot, player, discord_message)
        self.elemental = elemental


class StatusDetailView(Form):
    """
    A detail view for an Elemental on your team.
    """
    def __init__(self, options: StatusDetailOptions):
        super().__init__(options)
        self.elemental = options.elemental

    @property
    def buttons(self) -> List[Form.Button]:
        reactions = [BACK, ABILITIES, ATTRIBUTES, NICKNAME, NOTE]
        # No button values here. Non-default emojis will trigger different operations; see pick_option()
        return [Form.Button(reaction, None) for reaction in reactions]

    async def render(self) -> None:
        if not self.discord_message:
            self.discord_message = await self.bot.say(self.get_status())
        else:
            await self.bot.edit_message(self.discord_message, self.get_status())
        await self.bot.clear_reactions(self.discord_message)
        for button in self.buttons:
            await self.bot.add_reaction(self.discord_message, button.reaction)

    async def pick_option(self, reaction: str) -> None:
        if reaction == BACK:
            await self.back()
        elif reaction == ABILITIES:
            pass
        elif reaction == ATTRIBUTES:
            pass
        elif reaction == NICKNAME:
            pass
        elif reaction == NOTE:
            pass

    def get_status(self) -> str:
        # Renders HP, EXP, stats and currently active abilities and traits.
        elemental = self.elemental
        view = (f"{elemental.left_icon} {self.get_name()} "
                f"Lv. {elemental.level} (EXP: {elemental.current_exp} / {elemental.exp_to_level})\n"
                f"`{HealthBarView.from_elemental(elemental)} {elemental.current_hp} / {elemental.max_hp} HP`\n"
                f"{StatsView(elemental).get_view()}")
        note = f"Note: {elemental.note}" if elemental.note else ''
        option_descriptions = f"[⚔ Abilities]   [💪 Attributes]   [🏷 Nickname]   [📝 Note]"
        return '\n'.join([view, note, option_descriptions])

    def get_name(self) -> str:
        # If the Elemental has a nickname, also display its actual species name.
        name = self.elemental.name
        nickname = self.elemental.nickname
        if nickname != name:
            return f"**{nickname}** [{name}]"
        return f"**{name}**"

    async def back(self) -> None:
        """
        Rerenders the Status form.
        """
        await Form.from_form(self, StatusView)
