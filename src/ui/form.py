from typing import List

from src.core.constants import *
from src.elemental.elemental_factory import ElementalInitializer
from src.elemental.species.mithus import Mithus
from src.elemental.species.rainatu import Rainatu
from src.elemental.species.roaus import Roaus
from src.elemental.species.sithel import Sithel


class Form:
    """
    Logic behind rendering and updating options for an interface (represented by a Discord message)
    """

    def __init__(self, bot):
        self.bot = bot
        self.selected = []  # A list of all options that have been toggled. The actual selection is the last one.
        self.options = []  # List[Tuple]
        self.message = None

    async def render(self) -> None:
        raise NotImplementedError

    async def confirm(self):
        raise NotImplementedError

    async def pick_option(self, reaction: str) -> None:
        if reaction == OK:
            await self.confirm()
            return
        if reaction in self.options:
            self.selected.append(self.options.index(reaction))

    async def remove_option(self, reaction: str) -> None:
        if reaction in self.options:
            option = self.options.index(reaction)
            if option in self.selected:
                self.selected.pop(option)

    @staticmethod
    def static_options() -> List[str]:
        return [ONE, TWO, THREE, FOUR, FIVE, SIX]  # Reaction emojis that enumerate options.

    @property
    def _selected_item(self) -> int or None:
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
        message_body = f"{self.player.nickname}'s team: \n"
        for elemental in self.player.team.elementals:
            message_body += (f"{elemental.left_icon} {elemental.nickname}: "
                             f"{elemental.current_hp} / {elemental.max_hp} HP \n")
        self.message = await self.bot.say(message_body)
        for option in self.options:
            await self.bot.add_reaction(self.message, option)

    async def confirm(self):
        pass


class SelectStarter(Form):
    """
    The welcome screen where you choose an Elemental to start.
    """

    def __init__(self, bot, player):
        super().__init__(bot)
        self.player = player
        self.starters = [Rainatu(),
                         Mithus(),
                         Roaus(),
                         Sithel()]
        self.options = Form.static_options()[:len(self.starters)]
        self.options.append(OK)

    async def render(self) -> None:
        self.message = await self.bot.say('pls pik one')
        for option in self.options:
            await self.bot.add_reaction(self.message, option)

    async def confirm(self):
        """
        If you already have an elemental, this should do nothing.
        """
        if self.player.num_elementals > 0:
            return
        starter = self.starters[self._selected_item]
        self.player.add_elemental(ElementalInitializer.make(starter, level=3))
