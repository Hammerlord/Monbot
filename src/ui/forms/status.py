from typing import List

import discord
from discord.ext.commands import Bot

from src.core.constants import *
from src.elemental.ability.abilities.defend import Defend
from src.elemental.ability.ability import Ability
from src.elemental.attribute.attribute import Attribute
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
            await self._add_reaction(SWITCH)

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
        if reaction == SWITCH:
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
            await self._to_attributes_view()
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

    async def _to_attributes_view(self) -> None:
        options = StatusDetailOptions(self.bot, self.player, self.elemental, self.discord_message, self)
        form = AttributesView(options)
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
            await self._add_reaction(SWITCH)
        await self._add_reaction(BACK)

    @property
    def _view(self) -> str:
        elemental = self.elemental
        return '\n'.join([
            f"Lv. {elemental.level} {elemental.left_icon} {elemental.nickname}'s abilities",
            self.active_abilities,
            self.eligible_abilities
        ])

    @property
    def active_abilities(self) -> str:
        ability_views = ["**Currently active:**"]
        # Only visually enumerate active abilities if we have eligible abilities to swap.
        if self.elemental.eligible_abilities:
            for i, ability in enumerate(self.values):
                ability_views.append(f"{ValueForm.ORDERED_REACTIONS[i]} {AbilityOptionView(ability).get_detail()}")
        else:
            for ability in self.values:
                ability_views.append(AbilityOptionView(ability).get_detail())
        ability_views.append(AbilityOptionView(Defend()).get_detail())
        return '\n'.join(ability_views)

    @property
    def eligible_abilities(self) -> str:
        if self.elemental.eligible_abilities:
            return '\n'.join(["\n**Learned:**",
                              AbilityOptionView.detail_from_list(self.elemental.eligible_abilities),
                              f'\n{ABCD} `Swap an ability`   {SWITCH} `Swap all abilities`'])
        return ''

    async def pick_option(self, reaction: str) -> None:
        if reaction == BACK:
            await self._back()
            return
        await super().pick_option(reaction)
        if self._selected_value is not None or reaction == SWITCH:
            await self._to_switch_ability_view()

    async def _to_switch_ability_view(self) -> None:
        options = SwitchAbilityViewOptions(self.bot,
                                           self.player,
                                           self.elemental,
                                           self._selected_value,
                                           self.discord_message,
                                           self)
        form = SwitchAbilityView(options)
        await form.show()


class SwitchAbilityViewOptions(FormOptions):
    def __init__(self,
                 bot: Bot,
                 player,
                 elemental: Elemental,
                 selected_ability: Ability = None,
                 discord_message: discord.Message = None,
                 previous_form=None):
        super().__init__(bot, player, discord_message, previous_form)
        self.elemental = elemental
        self.selected_ability = selected_ability


class SwitchAbilityView(ValueForm):
    """
    A view to switch a single ability, or to select a new set of abilities.
    """

    def __init__(self, options: SwitchAbilityViewOptions):
        super().__init__(options)
        self._elemental = options.elemental
        self._selected_ability = options.selected_ability  # Ability or None; if None, we are swapping all abilities.

    @property
    def values(self) -> List[any]:
        if self._selected_ability is not None:
            return self._elemental.eligible_abilities
        # Else, show all abilities available for multiple selection.
        # Defend is automatically re-added, so we don't need it here.
        return [ability for ability in self._elemental.available_abilities if ability.name != 'Defend']

    @property
    def buttons(self) -> List[ValueForm.Button]:
        return self.ordered_buttons(self.values)

    async def render(self) -> None:
        await self._clear_reactions()
        await self._display(self._view)
        for button in self.buttons:
            await self._add_reaction(button.reaction)
        await self._add_reaction(BACK)

    @property
    def _view(self) -> str:
        view = []
        for i, ability in enumerate(self.values):
            view.append(f"{ValueForm.ORDERED_REACTIONS[i]} {AbilityOptionView(ability).get_detail()}")
        if self._selected_ability:
            view.append(f"```Select an ability to replace {self._selected_ability.name} "
                        f"for {self._elemental.nickname}```")
        else:
            view.append(self._multiple_selection_message)
        return '\n'.join(view)

    @property
    def _multiple_selection_message(self) -> str:
        max_num = self._elemental.max_active_abilities
        if self._is_selection_complete:
            return f"```Click [OK] to confirm this set.```"
        elif self._num_selections == 0:
            return (f"```Select a new set of abilities for {self._elemental.nickname}. "
                    f"({max_num} needed)```")
        return (f"```Currently selected: {', '.join([ability.name for ability in self._selected_values])} \n"
                f"({self._num_selections}/{max_num} needed)```")

    async def pick_option(self, reaction: str):
        if reaction == BACK:
            await self._back()
            return
        if reaction == OK and self._is_selection_complete:
            abilities = self._selected_values
            self._elemental.set_abilities(abilities)
            await self._back()
            return
        await super().pick_option(reaction)
        if self._selected_ability:
            eligible_ability = self._selected_value
            self._elemental.swap_ability(self._selected_ability, eligible_ability)
            await self._back()
        else:
            await self._display(self._view)
            if self._is_selection_complete:
                await self._add_reaction(OK)

    async def remove_option(self, reaction: str) -> None:
        super().remove_option(reaction)
        await self._display(self._view)

    @property
    def _num_selections(self) -> int:
        return len(self.toggled)

    @property
    def _is_selection_complete(self) -> bool:
        return self._num_selections == self._elemental.max_active_abilities


class AttributesView(ValueForm):
    """
    A view to spend an Elemental's Attribute points.
    """

    def __init__(self, options):
        super().__init__(options)
        self.elemental = options.elemental

    @property
    def buttons(self) -> List[ValueForm.Button]:
        return self.ordered_buttons(self.values)

    @property
    def values(self) -> List[any]:
        return self.elemental.attributes

    async def render(self) -> None:
        await self._display(self._view)
        await self._clear_reactions()
        selected_attribute = self._selected_value
        if selected_attribute:
            for reaction in [ADD, UP, CANCEL]:
                await self._add_reaction(reaction)
            return
        if self.elemental.has_attribute_points:
            for button in self.buttons:
                await self._add_reaction(button.reaction)
        await self._add_reaction(BACK)

    async def pick_option(self, reaction: str) -> None:
        if reaction == BACK:
            await self._back()
            return
        if reaction == CANCEL:
            self._clear_options()
            await self.render()
            return
        await super().pick_option(reaction)
        selected_attribute = self._selected_value
        if not selected_attribute:
            return
        if reaction == ADD:
            self.elemental.raise_attribute(selected_attribute)
        elif reaction == UP:
            for i in range(self.elemental.attribute_points):
                self.elemental.raise_attribute(selected_attribute)
        await self.render()

    @property
    def _view(self) -> str:
        view = [f"```{self.elemental.nickname}'s attributes```",
                self._attributes_list]
        if self.elemental.has_attribute_points:
            view.append(f"{self.elemental.attribute_points} points to assign. \n")
        selected_attribute = self._selected_value
        if selected_attribute:
            view.append(f"Selected: `{selected_attribute.name}`")
            view.append(f"{ADD} `+1 point`    {UP} `Add all pts`    {CANCEL} `Cancel`")
        return '\n'.join(view)

    @property
    def _attributes_list(self) -> str:
        view = []
        for i, attribute in enumerate(self.elemental.attributes):
            index = ValueForm.ORDERED_REACTIONS[i]
            stat_gained = f"[+{attribute.total_stat_gain()} {attribute.description}]" if attribute.level > 0 else ""
            header = f"{index} **{attribute.name}** Lv. {attribute.level} / {Attribute.MAX_LEVEL}  {stat_gained}\n"
            view.append(header)
            if attribute.can_level_up():
                view.append(f"Next rank: +{attribute.base_stat_gain} {attribute.description} \n")
        return ''.join(view)
