from src.core.constants import OK
from src.core.elements import Elements
from src.elemental.elemental_factory import ElementalInitializer
from src.elemental.species.mithus import Mithus
from src.elemental.species.rainatu import Rainatu
from src.elemental.species.roaus import Roaus
from src.elemental.species.sithel import Sithel
from src.elemental.species.species import Species
from src.ui.form import Form


class SelectStarter(Form):
    """
    The welcome screen where you choose an Elemental to start.
    """

    def __init__(self, bot, player):
        super().__init__(bot)
        self.player = player
        self.options = [Rainatu(),
                        Mithus(),
                        Roaus(),
                        Sithel()]
        self.buttons = Form.static_options()[:len(self.options)]
        self.buttons.append(OK)
        self.initial_render = True

    async def render_initial(self) -> None:
        self.message = await self.bot.say(self.get_initial_screen())
        for option in self.buttons:
            await self.bot.add_reaction(self.message, option)
        self.initial_render = False

    def get_initial_screen(self) -> str:
        message_body = ("```Welcome to the dangerous world of elementals!\n"
                        "It's impossible to go alone, so please take a companion with you.```")
        for i, starter in enumerate(self.options):
            message_body += self.get_starter_view(i, starter)
        return message_body

    async def render(self) -> None:
        if self.initial_render:
            await self.render_initial()
        elif len(self.selected) == 0:
            await self.bot.edit_message(self.message, self.get_initial_screen())
        else:
            index = self._selected_index
            species = self.options[index]
            await self.bot.edit_message(self.message, self.get_detail_screen(species))

    @staticmethod
    def get_detail_screen(starter: Species) -> str:
        abilities = starter.learnable_abilities[:2]  # Show two abilities.
        abilities_view = '\n'.join([f"{ability.icon} [{ability.name}] {ability.description}"
                                    for ability in abilities])

        return (f"{starter.left_icon} **{starter.name}**\n"
                f"{Elements.get_icon(starter.element)} type\n"
                f"*{starter.description}*\n"
                f"===== Abilities ===== \n"
                f"{abilities_view}"
                f"```Press OK to select this one.```")

    @staticmethod
    def get_starter_view(index: int, starter) -> str:
        return f"\n {index + 1}) {starter.left_icon} {starter.name}"

    async def pick_option(self, reaction: str) -> None:
        await super().pick_option(reaction)
        await self.render()

    async def remove_option(self, reaction: str) -> None:
        await super().remove_option(reaction)
        await self.render()

    async def confirm(self):
        if self.player.num_elementals > 0 or self._selected_index is None:
            return
        starter = self.options[self._selected_index]
        self.player.add_elemental(ElementalInitializer.make(starter, level=3))
