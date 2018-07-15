from typing import List

import discord
from discord.ext.commands import Bot

from src.core.constants import *
from src.elemental.elemental import Elemental
from src.ui.forms.form import Form, FormOptions, ValueForm
from src.ui.health_bar import HealthBarView
from src.ui.stats import StatsView


class StatusView(ValueForm):
    """
    Shows the status of your team.
    """
    def __init__(self, options: FormOptions):
        super().__init__(options)
        self.initial_render = True

    @property
    def values(self) -> List[Elemental]:
        return self.player.team.elementals

    @property
    def buttons(self) -> List[ValueForm.Button]:
        return self.enumerated_buttons(self.values)

    async def render(self) -> None:
        await self._clear_reactions()
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
            await self._create_detail_view(self._selected_value)

    async def _create_detail_view(self, elemental: Elemental) -> None:
        options = StatusDetailOptions(self.bot, self.player, elemental, self.discord_message)
        form = StatusDetailView(options)
        self.player.set_primary_view(form)
        await form.render()


class StatusDetailOptions(FormOptions):
    def __init__(self,
                 bot: Bot,
                 player,
                 elemental: Elemental,
                 discord_message: discord.Message = None):
        super().__init__(bot, player, discord_message)
        self.elemental = elemental


class StatusDetailView(Form):
    """
    A detail view for an Elemental on your team.
    """
    def __init__(self, options: StatusDetailOptions):
        super().__init__(options)
        self.elemental = options.elemental
        self.is_setting_nickname = False
        self.is_setting_note = False

    @property
    def is_awaiting_input(self) -> bool:
        return self.is_setting_note or self.is_setting_nickname

    async def render(self) -> None:
        await self._display(self.get_main_view())
        await self.bot.clear_reactions(self.discord_message)
        for reaction in [BACK, ABILITIES, ATTRIBUTES, NICKNAME, NOTE]:
            await self.bot.add_reaction(self.discord_message, reaction)

    async def pick_option(self, reaction: str) -> None:
        if self.is_awaiting_input:
            return
        if reaction == BACK:
            await self.back()
        elif reaction == ABILITIES:
            pass
        elif reaction == ATTRIBUTES:
            pass
        elif reaction == NICKNAME:
            await self.set_nickname_mode()
        elif reaction == NOTE:
            await self.set_note_mode()

    async def set_nickname_mode(self) -> None:
        self.is_setting_nickname = True
        await self._clear_reactions()
        message_body = (f"```Give {self.elemental.nickname} a new nickname. \n"
                        f"Awaiting input... Or type `;` to cancel.```"
                        f"{self.get_status()}")
        await self._display(message_body)

    async def set_note_mode(self) -> None:
        self.is_setting_note = True
        await self._clear_reactions()
        message_body = (f"```Set a note for {self.elemental.nickname}. \n"
                        f"Awaiting input... Or type `;` to cancel.```"
                        f"{self.get_status()}")
        await self._display(message_body)

    async def receive_input(self, message: discord.Message) -> None:
        content = message.content.strip()
        if content != ';':
            if self.is_setting_nickname:
                self.elemental.nickname = content
            elif self.is_setting_note:
                self.elemental.note = content
            await self.bot.add_reaction(message, OK_HAND)
        self.is_setting_nickname = False
        self.is_setting_note = False
        await self.render()

    def get_main_view(self) -> str:
        return '\n\n'.join([self.get_status(), self.option_descriptions])

    def get_status(self) -> str:
        """
        :return: str: HP, EXP, stats and currently active abilities and traits.
        """
        elemental = self.elemental
        note = f"```Note: {elemental.note}```" if elemental.note else ''
        return (f"{elemental.left_icon} {self.get_elemental_name()} "
                f"Lv. {elemental.level}  (EXP: {elemental.current_exp} / {elemental.exp_to_level})\n"
                f"`{HealthBarView.from_elemental(elemental)} {elemental.current_hp} / {elemental.max_hp} HP`\n"
                f"{note}"
                f"{StatsView(elemental).get_view()}")

    @property
    def option_descriptions(self) -> str:
        # Show what each reaction maps to.
        return (f"{ABILITIES}`Abilities`   "
                f"{ATTRIBUTES}`Attributes`   "
                f"{NICKNAME}`Nickname`   "
                f"{NOTE}`Note`")

    def get_elemental_name(self) -> str:
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
