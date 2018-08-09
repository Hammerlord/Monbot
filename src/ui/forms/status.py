from typing import List

import discord
from discord.ext.commands import Bot

from src.core.constants import *
from src.elemental.ability.abilities.defend import Defend
from src.elemental.elemental import Elemental
from src.ui.ability_option import AbilityOptionView
from src.ui.forms.form import Form, FormOptions, ValueForm
from src.ui.forms.inventory_form import ItemsView
from src.ui.health_bar import HealthBarView
from src.ui.stats import StatsView


class StatusView(ValueForm):
    """
    Shows the status of your team.
    """
    def __init__(self, options: FormOptions):
        super().__init__(options)
        self._selecting_leader_mode = False

    @property
    def values(self) -> List[Elemental]:
        return self.player.team.elementals

    @property
    def buttons(self) -> List[ValueForm.Button]:
        return self.ordered_buttons(self.values)

    async def render(self) -> None:
        await self._clear_reactions()
        await self._display(self._view)
        for button in self.buttons:
            await self._add_reaction(button.reaction)
        if self._selecting_leader_mode:
            await self._add_reaction(CANCEL)
            return
        await self._add_reaction(MEAT)
        if self.player.team.size > 1:
            await self._add_reaction(RETURN)

    @property
    def _view(self) -> str:
        message_body = f"```{self.player.nickname}'s team (Slots: {self.player.team.size}/4)```"
        for i, elemental in enumerate(self.values):
            message_body += self._get_status(i, elemental)
        if self._selecting_leader_mode:
            message_body += '```Select a new team leader, or click [X] to cancel.```'
        return message_body

    @staticmethod
    def _get_status(index: int, elemental: Elemental) -> str:
        return (f"{ValueForm.ORDERED_REACTIONS[index]} {elemental.left_icon}  "
                f"Lv. {elemental.level} {elemental.nickname}  "
                f"`{HealthBarView.from_elemental(elemental)} "
                f"{elemental.current_hp} / {elemental.max_hp} HP`  "
                f"`{elemental.current_exp} / {elemental.exp_to_level} EXP` \n")

    async def pick_option(self, reaction: str) -> None:
        if reaction == MEAT:
            await Form.from_form(self, ItemsView)
            return
        if reaction == RETURN:
            self._selecting_leader_mode = True
            await self.render()
            return
        if reaction == CANCEL:
            self._selecting_leader_mode = False
            await self.render()
            return
        await super().pick_option(reaction)
        if self._selected_value is None:
            return
        if self._selecting_leader_mode:
            await self._select_leader()
        else:
            await self._create_detail_view()

    async def _select_leader(self) -> None:
        elemental = self._selected_value
        self.player.team.set_leader(elemental)
        self._selecting_leader_mode = False
        await self.render()

    async def _create_detail_view(self) -> None:
        elemental = self._selected_value
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
        await self._display(self._view)
        await self._clear_reactions()
        await self._add_reactions([ABILITIES, ATTRIBUTES, NICKNAME, NOTE, BACK])

    async def pick_option(self, reaction: str) -> None:
        if self.is_awaiting_input:
            return
        if reaction == BACK:
            await self._back()
        elif reaction == ABILITIES:
            await self._to_ability_view()
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

    @property
    def _view(self) -> str:
        return '\n\n'.join([self.get_status(), self._option_descriptions])

    def get_status(self) -> str:
        """
        :return: str: HP, EXP, stats and currently active abilities and traits.
        """
        elemental = self.elemental
        note = f"```Note: {elemental.note}```" if elemental.note else ''
        return (f"{elemental.left_icon} {self._get_elemental_name()} "
                f"Lv. {elemental.level}  (EXP: {elemental.current_exp} / {elemental.exp_to_level})\n"
                f"`{HealthBarView.from_elemental(elemental)} {elemental.current_hp} / {elemental.max_hp} HP`\n"
                f"{note}"
                f"{StatsView(elemental).get_view()}")

    @property
    def _option_descriptions(self) -> str:
        # Show what each reaction maps to.
        return (f"{ABILITIES}`Abilities`   "
                f"{ATTRIBUTES}`Attributes`   "
                f"{NICKNAME}`Nickname`   "
                f"{NOTE}`Note`")

    def _get_elemental_name(self) -> str:
        # If the Elemental has a nickname, also display its actual species name.
        name = self.elemental.name
        nickname = self.elemental.nickname
        if nickname != name:
            return f"**{nickname}** [{name}]"
        return f"**{name}**"

    async def _to_ability_view(self) -> None:
        options = StatusDetailOptions(self.bot, self.player, self.elemental, self.discord_message, self)
        form = AbilitiesView(options)
        await form.show()


class AbilitiesView(ValueForm):
    """
    A view showing all the currently-learned abilities for a particular elemental.
    Allows users to swap active abilities.
    """
    def __init__(self, options: StatusDetailOptions):
        super().__init__(options)
        self.elemental = options.elemental

    @property
    def values(self) -> List[any]:
        # Defend cannot be switched out.
        return [ability for ability in self.elemental.active_abilities if ability.name != 'Defend']

    @property
    def buttons(self) -> List[ValueForm.Button]:
        return self.ordered_buttons(self.values)

    async def render(self) -> None:
        await self._display(self._view)
        await self._clear_reactions()
        if self.elemental.eligible_abilities:
            for button in self.buttons:
                await self._add_reaction(button.reaction)
            await self._add_reaction(RETURN)
        await self._add_reaction(BACK)

    @property
    def _view(self) -> str:
        elemental = self.elemental
        return '\n'.join([
            f"Lv. {elemental.level} {elemental.left_icon} {elemental.nickname}'s abilities\n",
            self.active_abilities,
            self.eligible_abilities
         ])

    @property
    def active_abilities(self) -> str:
        ability_views = ["**Currently active:**"]
        # Only visibly enumerate the abilities if we have eligible abilities to swap.
        if self.elemental.eligible_abilities:
            for i, ability in enumerate(self.values):
                ability_views.append(f"{ValueForm.ORDERED_REACTIONS[i]} {AbilityOptionView(ability).get_detail()}")
        else:
            for ability in self.values:
                ability_views.append(f"{AbilityOptionView(ability).get_detail()}")
        ability_views.append(AbilityOptionView(Defend()).get_detail())
        return '\n'.join(ability_views)

    @property
    def eligible_abilities(self) -> str:
        if self.elemental.eligible_abilities:
            return '\n'.join(["**Learned:**",
                              AbilityOptionView.detail_from_list(self.elemental.eligible_abilities),
                              f'{ABCD} `Swap an ability`   {RETURN} `Swap all abilities`'])
        return ''

    async def _pick_option(self, reaction: str):
        if reaction == BACK:
            await self._back()
            return
