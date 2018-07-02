from src.core.constants import *


class Form:
    """
    Logic behind rendering and updating options for an interface (represented by a Discord message)
    """
    STATIC_OPTIONS = [ONE, TWO, THREE, FOUR, FIVE, SIX]  # Reaction emojis that enumerate options.

    def __init__(self, bot):
        self.bot = bot
        self.selected = []  # A list of all options that have been toggled. The actual selection is the last one.
        self.options = []  # List[Tuple]
        self.message = None

    async def render(self) -> None:
        raise NotImplementedError

    async def confirm(self):
        raise NotImplementedError

    async def pick_option(self, reaction: str):
        if reaction == OK:
            await self.confirm()
            return
        for option in self.options:
            if option[0] == reaction:
                self.selected.append(option[1])

    async def remove_option(self, reaction: str):
        for option in self.options:
            if option[0] == reaction:
                self.selected.pop(option[1])


class Status(Form):
    """
    Shows the status of your team.
    """
    def __init__(self, bot, player):
        super().__init__(bot)
        self.player = player
        self.options = [(Form.STATIC_OPTIONS[i], i) for i in range(player.team.size)]

    async def render(self) -> None:
        message_body = f"{self.player.nickname}'s team: \n"
        for elemental in self.player.team.elementals:
            message_body += (f"{elemental.left_icon} {elemental.nickname}: "
                             f"{elemental.current_hp} / {elemental.max_hp} HP \n")
        self.message = await self.bot.say(message_body)
        for option in self.options:
            await self.bot.add_reaction(self.message, option[0])

    async def confirm(self):
        pass


class SelectStarter(Form):
    """
    The welcome screen where you choose an Elemental to start.
    """
    def __init__(self, bot):
        super().__init__(bot)
        self.options = [(ONE,),
                        (TWO,),
                        (THREE,),
                        (OK,)]  # TODO tuple...

    async def render(self) -> None:
        self.message = await self.bot.say('pls pik one')
        for option in self.options:
            emoji = option[0]
            await self.bot.add_reaction(self.message, emoji)

    async def confirm(self):
        """
        When you click ok, it should create a profile with your most recently selected elemental.
        If you already have a profile, this should do nothing.
        :return:
        """
        pass
