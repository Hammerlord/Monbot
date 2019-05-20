import asyncio
from typing import List

import discord
from discord.ext.commands import Bot

from src.character.inventory import Item, ItemSlot
from src.character.player import Player
from src.core.constants import BACK
from src.data.data_manager import DataManager
from src.elemental.elemental import Elemental
from src.items.consumables import Consumable
from src.items.item import ItemTypes
from src.ui.forms.form import ValueForm, FormOptions, Form
from src.ui.health_bar import HealthBarView


class ItemsView(ValueForm):
    """
    Displays the items in your inventory (materials and consumables).
    For the in-combat inventory, see battle.py.
    """

    def __init__(self, options: FormOptions):
        super().__init__(options)

    @property
    def values(self) -> List[ItemSlot]:
        return self.player.items

    @property
    def buttons(self) -> List[ValueForm.Button]:
        return [ValueForm.Button(item_slot.item.icon, item_slot.item) for item_slot in self.values]

    async def render(self) -> None:
        await self._clear_reactions()
        await self._display(self._view)
        for button in self.buttons:
            await self._add_reaction(button.reaction)
        await self._add_reaction(BACK)

    @property
    def _view(self) -> str:
        return (f"```{self.player.nickname}'s bag```"
                f"{self._item_views}")

    @property
    def _item_views(self) -> str:
        return '\n'.join([f"{slot.item.icon} **{slot.item.name} x{slot.amount}** {slot.item.properties}"
                          for slot in self.values])

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
        if not self.player.has_item(self.item):
            await asyncio.sleep(1.5)
            await self._back()
            return
        for button in self.buttons:
            await self._add_reaction(button.reaction)
        await self._add_reaction(BACK)

    @property
    def _view(self) -> str:
        items_left = self.player.inventory.amount_left(self.item)
        return (f"Selected **{self.item.icon} {self.item.name} ({items_left} left)** \n"
                f"{self._display_item_properties(self.item)} \n {self._eligible_elementals}")

    @staticmethod
    def _display_item_properties(consumable: 'Consumable' or 'Item') -> str:
        """
        :return: A string displaying the various properties of a consumable for rendering purposes.
        """
        properties = []
        if consumable.resurrects_target:
            properties.append("[Revives KO]")
        if consumable.healing_percentage:
            properties.append(f"[+{int(consumable.healing_percentage * 100)}% HP]")
        if consumable.exp_gained_on_use:
            properties.append(f"[+{consumable.exp_gained_on_use} EXP]")
        return ' '.join(properties)

    @property
    def _eligible_elementals(self) -> str:
        if len(self.values) == 0:
            return "```(You don't have anyone to use this item on.)```"
        message_body = ''
        for i, elemental in enumerate(self.values):
            message_body += self._get_status(i, elemental)
        if self.recently_affected_elemental:
            message_body += f"```Gave {self.item.name} to {self.recently_affected_elemental.nickname}.```"
        elif self.player.has_item(self.item):
            message_body += f"```Give {self.item.name} to who?```"
        return message_body

    def _get_status(self, index: int, elemental: Elemental) -> str:
        feedback = ':heart:' if self.recently_affected_elemental == elemental else ''
        return (f"{index + 1}) {elemental.left_icon}  Lv. {elemental.level} {elemental.nickname}  "
                f"`{HealthBarView.from_elemental(elemental)} "
                f"{elemental.current_hp} / {elemental.max_hp} HP`  "
                f"`{elemental.current_exp} / {elemental.exp_to_level} EXP` {feedback}\n")

    async def pick_option(self, reaction: str) -> None:
        if reaction == BACK:
            await self._back()
            return
        await super().pick_option(reaction)
        elemental = self._selected_value
        if elemental is not None:
            if self.player.use_item(self.item, elemental):
                self.recently_affected_elemental = elemental
                self._save()
                await self.render()

    def _save(self) -> None:
        data_manager = DataManager()
        data_manager.update_inventory(self.player)
        data_manager.update_elemental(self.recently_affected_elemental)
