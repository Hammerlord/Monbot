from typing import List

from src.core.constants import OK
from src.core.elements import Elements
from src.elemental.elemental_factory import ElementalInitializer
from src.elemental.species.mithus import Mithus
from src.elemental.species.rainatu import Rainatu
from src.elemental.species.roaus import Roaus
from src.elemental.species.sithel import Sithel
from src.elemental.species.species import Species
from src.ui.ability_option import AbilityOptionView
from src.ui.forms.form import Form, FormOptions, ValueForm
from src.ui.forms.status import StatusView


class SelectStarterView(ValueForm):
    """
    The welcome screen where you choose an Elemental to start.
    """

    def __init__(self, options: FormOptions):
        super().__init__(options)
        self.initial_render = True

    @property
    def values(self) -> List[Species]:
        return [Rainatu(), Mithus(), Roaus(), Sithel()]

    @property
    def buttons(self) -> List[ValueForm.Button]:
        return self.enumerated_buttons(self.values)

    async def render(self) -> None:
        if self.initial_render:
            await self.render_initial()
        elif len(self.toggled) == 0:
            await self._display(self._get_initial_page())
        else:
            species = self._selected_value
            await self._display(self._get_detail_page(species))

    async def render_initial(self) -> None:
        await self._display(self._get_initial_page())
        for button in self.buttons:
            await self.bot.add_reaction(self.discord_message, button.reaction)
        self.initial_render = False

    async def pick_option(self, reaction: str) -> None:
        if reaction == OK:
            await self._confirm()
            return
        is_valid_pick = await super().pick_option(reaction)
        if is_valid_pick:
            await self.render()
            # If there's a valid selection, we add an OK button.
            # The selection can become invalidated afterward, in which case OK safely does nothing.
            await self.bot.add_reaction(self.discord_message, OK)

    async def remove_option(self, reaction: str) -> None:
        is_valid_removal = await super().remove_option(reaction)
        if is_valid_removal:
            await self.render()

    def _get_initial_page(self) -> str:
        message_body = ("```Welcome to the dangerous world of elementals!\n"
                        "It's impossible to go alone, so please take a companion with you.```")
        for i, starter in enumerate(self.values):
            message_body += f"{i + 1}) {starter.left_icon} {starter.name}\n"
        return message_body

    @staticmethod
    def _get_detail_page(starter: Species) -> str:
        abilities = starter.learnable_abilities[:2]  # Show two abilities.
        abilities_view = AbilityOptionView.detail_from_list(abilities)

        return (f"{starter.left_icon} **{starter.name}** [{Elements.get_icon(starter.element)} type]\n"
                f"{starter.description}\n\n"
                f"{abilities_view}")

    async def _confirm(self):
        if self.player.num_elementals > 0 or self._selected_value is None:
            return
        starter = self._selected_value
        self.player.add_elemental(ElementalInitializer.make(starter, level=3))
        await Form.from_form(self, StatusView)
