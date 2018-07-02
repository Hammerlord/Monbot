from typing import List

from src.core.constants import *
from src.elemental.elemental import Elemental
from src.ui.health_bar import HealthBarView


class Form:
    """
    Logic behind rendering and updating options for an interface (represented by a Discord message).
    Reactions act as controls to manipulate views and state.
    """

    def __init__(self, bot):
        self.bot = bot
        self.selected = []  # List[int] A list of all selected indices. The actual selection is the last one.
        self.buttons = []  # List[str]
        self.options = []  # List[any] The option values, mapped to each button.
        self.message = None

    async def render(self) -> None:
        raise NotImplementedError

    async def confirm(self):
        raise NotImplementedError

    async def pick_option(self, reaction: str) -> None:
        if reaction == OK:
            await self.confirm()
            return
        if reaction in self.buttons:
            self.selected.append(self.buttons.index(reaction))

    async def remove_option(self, reaction: str) -> None:
        if reaction in self.buttons:
            option = self.buttons.index(reaction)
            if option in self.selected:
                self.selected.remove(option)

    @staticmethod
    def static_options() -> List[str]:
        return [ONE, TWO, THREE, FOUR, FIVE, SIX]  # Reaction emojis that enumerate options.

    @property
    def _selected_index(self) -> int or None:
        """
        :return: int: The selected item is the option most recently toggled. Or None, if none are toggled.
        """
        if len(self.selected) == 0:
            return None
        return self.selected[-1]


class Status(Form):
    """
    Shows the status of your team.
    """

    def __init__(self, bot, player):
        super().__init__(bot)
        self.player = player
        self.options = Form.static_options()[:player.team.size]

    async def render(self) -> None:
        message_body = f"```{self.player.nickname}'s Team```"
        for i, elemental in enumerate(self.player.team.elementals):
            message_body += self._get_status(i, elemental)
        self.message = await self.bot.say(message_body)
        for option in self.options:
            await self.bot.add_reaction(self.message, option)

    @staticmethod
    def _get_status(index: int, elemental: Elemental) -> str:
        return (f"{index + 1}) `{elemental.left_icon} {elemental.nickname} "
                f"{HealthBarView.from_elemental(elemental)} "
                f"{elemental.current_hp} / {elemental.max_hp} HP` \n")

    async def confirm(self):
        # No operation.
        pass

