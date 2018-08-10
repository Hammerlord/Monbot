from collections import namedtuple
from typing import List

from discord.ext.commands import Bot
import discord
from src.core.constants import *


class FormOptions:
    """
    The dependencies of a Form.
    """

    def __init__(self,
                 bot: Bot,
                 player,
                 discord_message: discord.Message = None,
                 previous_form: 'Form' = None):
        self.bot = bot
        self.player = player
        self.discord_message = discord_message  # Optional. The form will edit an existing message.
        self.previous_form = previous_form


class Form:
    """
    Logic for rendering and updating options in an interface (represented by a Discord message).
    Reactions act as controls to manipulate views and state.
    Each new set of reactions should have their own form.
    """

    def __init__(self, options: FormOptions):
        self.bot = options.bot
        self.player = options.player
        self.discord_message = options.discord_message  # The Discord.message object representing this form.
        self.previous_form = options.previous_form

    @property
    def is_awaiting_input(self) -> bool:
        """
        Override this with the condition which a form would await a user's typed input.
        Also remember to implement a way to switch it off.
        """
        return False

    def matches(self, other: discord.Message) -> bool:
        """
        To check if a reaction added onto a message corresponds to the one in this Form.
        """
        return self.discord_message.id == other.id

    async def render(self) -> None:
        """
        Tell the bot to render a message body depending on the state.
        """
        raise NotImplementedError

    async def pick_option(self, reaction: str) -> bool:
        """
        Called when a user clicks a reaction (on_reaction_add event).
        """
        raise NotImplementedError

    async def _display(self, message: str) -> None:
        """
        Helper method to edit the discord message if one exists, or set a message if not.
        :param message: The message body.
        """
        if self.discord_message:
            try:
                await self.bot.edit_message(self.discord_message, message)
            except discord.errors.NotFound:
                print("Message has been deleted.")
        else:
            self.discord_message = await self.bot.say(message)

    async def _add_reactions(self, reactions: List[str]) -> None:
        for reaction in reactions:
            if not await self._add_reaction(reaction):
                return

    async def _add_reaction(self, reaction: str) -> bool:
        try:
            await self.bot.add_reaction(self.discord_message, reaction)
            return True
        except discord.errors.NotFound:
            print("Message has been deleted.")

    async def remove_option(self, reaction: str) -> bool:
        # No op. Removing a reaction doesn't do anything by default.
        pass

    async def _clear_reactions(self) -> None:
        """
        Attempt to clear reactions from the message.
        TODO should delete the message and repost if we don't have permission to clear reactions.
        """
        if self.discord_message:
            try:
                await self.bot.clear_reactions(self.discord_message)
            except discord.errors.NotFound:
                print("Message has been deleted.")

    def get_form_options(self) -> FormOptions:
        return FormOptions(self.bot,
                           self.player,
                           self.discord_message,
                           previous_form=self)

    @staticmethod
    async def from_form(from_form: 'Form', to_form) -> None:
        """
        Creates a form from another form, allowing the same Discord message to be reused.
        :param from_form: The old form to take dependencies from.
        :param to_form: Reference to the Form class being generated
        """
        options = from_form.get_form_options()
        new_form = to_form(options)
        options.player.set_primary_view(new_form)
        await new_form.render()

    async def show(self) -> None:
        self.player.set_primary_view(self)
        await self.render()

    async def _back(self) -> None:
        if self.previous_form:
            await self.previous_form.show()


class ValueForm(Form):
    """
    A type of form that allows multiple selection of choices by implementing pick_option.
    """
    Button = namedtuple('Button', 'reaction, value')
    ORDERED_REACTIONS = [A, B, C, D, E, F, G, H, I, J, K, L, M, N, O, P, Q, R, S]
    ENUMERATED_REACTIONS = [ONE, TWO, THREE, FOUR, FIVE, SIX, SEVEN, EIGHT, NINE, TEN]

    def __init__(self, options: FormOptions):
        super().__init__(options)
        self.toggled = []  # Type: List[Button] The "toggled on" buttons.

    def render(self) -> None:
        raise NotImplementedError

    @property
    def values(self) -> List[any]:
        """
        :return: Values (any) to be mapped to reactions.
        """
        raise NotImplementedError

    @property
    def buttons(self) -> List[Button]:
        """
        :return: A list of buttons, which are emoji strings mapped to values.
        """
        raise NotImplementedError

    async def pick_option(self, reaction: str) -> bool:
        """
        Adds the selected button to this.toggled. Later used to retrieve what the user picked.
        :return: True if a valid option was added.
        """
        for button in self.buttons:
            if button.reaction == reaction:
                self.toggled.append(button)
                return True

    async def remove_option(self, reaction: str) -> bool:
        """
        Removes the button from this.toggled.
        :return: True if a valid option was removed.
        """
        for button in self.toggled:
            if button.reaction == reaction:
                self.toggled.remove(button)
                return True

    @staticmethod
    def enumerated_buttons(values: List[any]) -> List[Button]:
        # Creates buttons with reaction emojis that enumerate values.
        # For now, this gets around the issues of duplicates and needing custom icons.
        return [ValueForm.Button(ValueForm.ENUMERATED_REACTIONS[i], value) for i, value in enumerate(values)]

    @staticmethod
    def ordered_buttons(values: List[any]) -> List[Button]:
        # Creates buttons with alphabeticized emojis. There are more emojis in this set.
        return [ValueForm.Button(ValueForm.ORDERED_REACTIONS[i], value) for i, value in enumerate(values)]

    @property
    def _selected_value(self) -> any or None:
        """
        :return: The value object of the most recently toggled button.
        """
        if len(self.toggled) > 0:
            return self.toggled[-1].value

    @property
    def _selected_values(self) -> List[any] or None:
        """
        Values of all toggled buttons.
        """
        if len(self.toggled) > 0:
            return [toggled.value for toggled in self.toggled]