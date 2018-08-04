from typing import List

import asyncio
import discord
from discord.ext.commands import Bot

from src.character.inventory import ItemSlot, Item
from src.character.player import Player
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
            await self._add_reaction(button.reaction)
        await self._add_reaction(ITEM)
        if self.player.team.size > 1:
            await self._add_reaction(RETURN)

    def _get_page(self) -> str:
        message_body = f"```{self.player.nickname}'s team (Slots: {self.player.team.size}/4)```"
        for i, elemental in enumerate(self.values):
            message_body += self._get_status(i, elemental)
        return message_body

    @staticmethod
    def _get_status(index: int, elemental: Elemental) -> str:
        return (f"{index + 1}) {elemental.left_icon}  Lv. {elemental.level} {elemental.nickname}  "
                f"`{HealthBarView.from_elemental(elemental)} "
                f"{elemental.current_hp} / {elemental.max_hp} HP`  "
                f"{elemental.current_exp} / {elemental.exp_to_level} EXP \n")

    async def pick_option(self, reaction: str) -> None:
        if reaction == ITEM:
            await Form.from_form(self, ItemsView)
            return
        if reaction == RETURN:
            return
        await super().pick_option(reaction)
        if self._selected_value is not None:
            await self._create_detail_view(self._selected_value)

    async def _create_detail_view(self, elemental: Elemental) -> None:
        options = StatusDetailOptions(self.bot, self.player, elemental, self.discord_message, self)
        form = StatusDetailView(options)
        await form.show()


class StatusDetailOptions(FormOptions):
    def __init__(self,
                 bot: Bot,
                 player,
                 elemental: Elemental,
                 discord_message: discord.Message = None,
                 previous_form=None):
        super().__init__(bot, player, discord_message, previous_form)
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
        await self._clear_reactions()
        await self._add_reactions([ABILITIES, ATTRIBUTES, NICKNAME, NOTE, BACK])

    async def pick_option(self, reaction: str) -> None:
        if self.is_awaiting_input:
            return
        if reaction == BACK:
            await self._back()
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


class ItemsView(ValueForm):
    """
    Displays the items in your inventory. TODO only consumables are usable.
    """
    def __init__(self, options: FormOptions):
        super().__init__(options)

    @property
    def values(self) -> List[ItemSlot]:
        return self.player.inventory.items

    @property
    def buttons(self) -> List[ValueForm.Button]:
        return [ValueForm.Button(item_slot.item.icon, item_slot.item) for item_slot in self.values
                if item_slot.amount > 0]

    async def render(self) -> None:
        await self._clear_reactions()
        await self._display(self._get_view())
        for button in self.buttons:
            await self._add_reaction(button.reaction)
        await self._add_reaction(BACK)

    def _get_view(self) -> str:
        view = f"```{self.player.nickname}'s bag```"
        view += self._item_views
        return view

    @property
    def _item_views(self) -> str:
        item_slots = []
        for slot in self.values:
            if slot.amount == 0:
                continue
            view = (f"{slot.item.icon} **{slot.item.name} x{slot.amount}** {slot.item.properties} \n "
                    f"{slot.item.description}")
            item_slots.append(view)
        return '\n'.join(item_slots)

    async def pick_option(self, reaction: str) -> None:
        if reaction == BACK:
            await self._back()
            return
        await super().pick_option(reaction)
        item = self._selected_value
        if item is not None:
            options = UseItemOptions(self.bot, self.player, item, self.discord_message, self)
            form = UseItemView(options)
            await form.show()


class UseItemOptions(FormOptions):
    def __init__(self,
                 bot: Bot,
                 player: Player,
                 item: Item,
                 discord_message: discord.Message = None,
                 previous_form: Form = None):
        super().__init__(bot, player, discord_message, previous_form)
        self.item = item


class UseItemView(ValueForm):
    """
    Pick a member of your current team to use an item on.
    """
    def __init__(self, options: UseItemOptions):
        super().__init__(options)
        self.item = options.item
        self.inventory = self.player.inventory
        self.recently_affected_elemental = None

    @property
    def values(self) -> List[Elemental]:
        """
        Only show elementals who are eligible for the item's effect.
        """
        return [elemental for elemental in self.player.team.elementals if self.item.is_usable_on(elemental)]

    @property
    def buttons(self) -> List[ValueForm.Button]:
        return self.enumerated_buttons(self.values)

    async def render(self) -> None:
        await self._display(self._view)
        self.recently_affected_elemental = None
        await self._clear_reactions()
        if self.inventory.amount_left(self.item) == 0:
            await asyncio.sleep(1.5)
            await self._back()
            return
        for button in self.buttons:
            await self._add_reaction(button.reaction)
        await self._add_reaction(BACK)

    @property
    def _view(self) -> str:
        items_left = self.inventory.amount_left(self.item)
        return (f"Selected **{self.item.icon} {self.item.name} ({items_left} left)** \n"
                f"{self.item.properties} \n {self._eligible_elementals}")

    @property
    def _eligible_elementals(self) -> str:
        if len(self.values) == 0:
            return "```(You don't have anyone to use this item on.)```"
        message_body = ''
        items_left = self.inventory.amount_left(self.item)
        for i, elemental in enumerate(self.values):
            message_body += self._get_status(i, elemental)
        if self.recently_affected_elemental:
            message_body += f"```Gave {self.item.name} to {self.recently_affected_elemental.nickname}.```"
        elif items_left > 0:
            message_body += f"```Give {self.item.name} to who?```"
        return message_body

    def _get_status(self, index: int, elemental: Elemental) -> str:
        feedback = ':heart:' if self.recently_affected_elemental == elemental else ''
        return (f"{index + 1}) {elemental.left_icon}  Lv. {elemental.level} {elemental.nickname}  "
                f"`{HealthBarView.from_elemental(elemental)} "
                f"{elemental.current_hp} / {elemental.max_hp} HP`  "
                f"{elemental.current_exp} / {elemental.exp_to_level} EXP {feedback}\n")

    async def pick_option(self, reaction: str) -> None:
        if reaction == BACK:
            await self._back()
            return
        await super().pick_option(reaction)
        elemental = self._selected_value
        if elemental is not None:
            if self.inventory.use_item(self.item, elemental):
                self.recently_affected_elemental = elemental
                await self.render()
