from collections import namedtuple
from typing import List

from src.core.constants import *


class Form:
    """
    Logic for rendering and updating options in an interface (represented by a Discord message).
    Reactions act as controls to manipulate views and state.
    Each new set of reactions should have their own form.
    """

    Button = namedtuple('Button', 'reaction, value')

    def __init__(self, bot, message=None):
        self.bot = bot
        self.toggled: List[Form.Button] = []  # The "toggled on" buttons.
        self.values: List[any] = []  # Values to be mapped to the reactions, if applicable.
        self.discord_message = message  # The Discord.message object representing this form.

    @property
    def buttons(self) -> List[Button]:
        """
        :return: A list of emojis used to render buttons (reactions).
        """
        raise NotImplementedError

    async def render(self) -> None:
        """
        Tell the bot to render a message body depending on the state.
        """
        raise NotImplementedError

    async def pick_option(self, reaction: str) -> bool:
        """
        Adds the index of the valid button to this.toggled. Later used to retrieve what the user picked.
        :return: True if a valid option was added.
        """
        for button in self.buttons:
            if button.reaction == reaction:
                self.toggled.append(button)
                return True

    async def remove_option(self, reaction: str) -> bool:
        """
        Removes the index of the button from this.selected.
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
        reactions = [ONE, TWO, THREE, FOUR, FIVE, SIX]
        return [Form.Button(reactions[i], value) for i, value in enumerate(values)]

    @property
    def _selected_value(self) -> any or None:
        """
        :return: The value object of the most recently toggled button.
        """
        if len(self.toggled) > 0:
            return self.toggled[-1].value

    async def _display(self, message: str) -> None:
        """
        Helper method to edit the discord message if one exists, or set a message if not.
        :param message: The message body.
        """
        if self.discord_message:
            await self.bot.edit_message(self.discord_message, message)
        else:
            self.discord_message = await self.bot.say(message)
