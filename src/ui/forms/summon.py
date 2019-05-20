from typing import List

import discord
from discord.ext.commands import Bot

from src.core.config import SHARDS_TO_SUMMON
from src.core.constants import BACK, OK, SUMMON, STATUS
from src.core.elements import Elements
from src.data.data_manager import DataManager
from src.elemental.elemental import Elemental
from src.elemental.elemental_factory import ElementalInitializer
from src.items.shards import ManaShard
from src.ui.forms.form import ValueForm, FormOptions, Form
from src.ui.health_bar import HealthBarView
from src.ui.stats import StatsView


class SummonMenuOptions(FormOptions):
    def __init__(self,
                 bot: Bot,
                 player,
                 data_manager: DataManager,
                 discord_message: discord.Message = None,
                 previous_form: 'Form' = None):
        super().__init__(bot, player, discord_message, previous_form)
        self.data_manager = data_manager


class SummonMenu(ValueForm):
    def __init__(self, options):
        """
        :param options: SaveableDataViewOptions
        """
        super().__init__(options)
        self.data_manager = options.data_manager

    async def render(self) -> None:
        await self._clear_reactions()
        await self._display(self._view)
        if self._can_summon():
            await self._add_reaction(SUMMON)
            for button in self.buttons:
                await self._add_reaction(button.reaction)
        await self._add_reaction(BACK)

    @property
    def _view(self) -> str:
        view = [f"```Summon an elemental.```",
                f"Reagents needed: {ManaShard().icon} `Mana Shard` x3   ",
                f"Owned: {self.player.inventory.amount_left(ManaShard())}",
                f"Optional: Adding an elemental shard guarantees the element of your summon.",
                self._shards_owned,
                self._selected_element_view]
        return '\n'.join(view)

    @property
    def _selected_element_view(self) -> str:
        if not self._can_summon():
            return ''
        if self._selected_value:
            return f'\nSelected element: {self._selected_value.name} - Click {SUMMON} to summon.'
        return f'\nClick {SUMMON} to summon.'

    @property
    def _shards_owned(self) -> str:
        shards = self._shards_view
        return f'Owned: {shards}' if shards else '*(You have no elemental shards)*'

    @property
    def _shards_view(self) -> str:
        view = []
        for shard in self.player.inventory.shards:
            if shard.name != ManaShard().name:
                view.append(f"{shard.icon} `x{shard.amount}`")
        return '   '.join(view) if view else ''

    @property
    def buttons(self) -> List[ValueForm.Button]:
        return [ValueForm.Button(shard.icon, shard) for shard in self.values]

    @property
    def values(self) -> List[any]:
        return [shard for shard in self.player.inventory.shards if shard.name != ManaShard().name]

    async def pick_option(self, reaction: str) -> None:
        await super().pick_option(reaction)
        if reaction == BACK:
            # Go back to main menu, not summon results
            pass
        if reaction == SUMMON and self._can_summon():
            await self._summon()

    async def _summon(self) -> None:
        player = self.player
        player.inventory.remove_item(ManaShard(), SHARDS_TO_SUMMON)
        elemental = ElementalInitializer.make_random(player.level, player.elementals, self._selected_element)
        player.add_elemental(elemental)
        self.data_manager.update_player(self.player)
        self.data_manager.update_elemental(elemental)

    @property
    def _selected_element(self) -> Elements:
        if self._selected_value:  # Type ItemSlot
            return self._selected_value.item.element

    def _can_summon(self) -> bool:
        return self.player.inventory.amount_left(ManaShard()) >= SHARDS_TO_SUMMON


class ElementalViewOptions(FormOptions):
    def __init__(self,
                 bot: Bot,
                 player,
                 elemental: Elemental,
                 discord_message: discord.Message = None,
                 previous_form=None):
        super().__init__(bot, player, discord_message, previous_form)
        self.elemental = elemental


class SummonResultsView(Form):

    def __init__(self, options: ElementalViewOptions):
        super().__init__(options)
        self.elemental = options.elemental

    async def render(self) -> None:
        await self._clear_reactions()
        await self._display(self._view)
        await self._add_reaction(STATUS)
        if self._can_summon():
            await self._add_reaction(SUMMON)

    @property
    def _view(self) -> str:
        elemental = self.elemental
        view = ["```Another elemental has become your campanion.```",
                f"Lv. {elemental.level} {elemental.left_icon} {elemental.name}",
                f"Type: {elemental.element}",
                f"`{HealthBarView.from_elemental(elemental)} {elemental.current_hp} / {elemental.max_hp} HP`",
                StatsView(elemental).get_view(),
                self._render_options]
        return '\n'.join(view)

    @property
    def _render_options(self) -> str:
        view = [f"\n{STATUS} `status`"]
        if self._can_summon():
            view.append(f"{SUMMON} `summon again`")
        return "   ".join(view)

    async def pick_option(self, reaction: str) -> None:
        if reaction == STATUS:
            # Elementals, not team
            pass
        elif reaction == SUMMON:
            self.previous_form.discord_message = self.discord_message
            await self.previous_form.show()

    def _can_summon(self) -> bool:
        return self.player.inventory.amount_left(ManaShard()) >= SHARDS_TO_SUMMON
