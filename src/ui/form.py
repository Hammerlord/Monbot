from typing import List

from src.core.constants import *


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

