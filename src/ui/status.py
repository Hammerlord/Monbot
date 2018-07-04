from typing import List

from src.elemental.elemental import Elemental
from src.ui.form import Form
from src.ui.health_bar import HealthBarView
from src.ui.stats import StatsView


class StatusView(Form):
    """
    Shows the status of your team.
    """
    def __init__(self,
                 bot,
                 player):
        super().__init__(bot)
        self.player = player
        self.values: List[Elemental] = self.player.team.elementals
        self.initial_render = True

    @property
    def buttons(self) -> List[Form.Button]:
        return self.enumerated_buttons(self.values)

    async def render(self) -> None:
        message_body = f"```{self.player.nickname}'s Team (Slots: {self.player.team.size}/4)```"
        for i, elemental in enumerate(self.values):
            message_body += self._get_status(i, elemental)
        self.discord_message = await self.bot.say(message_body)
        for button in self.buttons:
            await self.bot.add_reaction(self.discord_message, button.reaction)

    @staticmethod
    def _get_status(index: int, elemental: Elemental) -> str:
        return (f"{index + 1}) {elemental.left_icon}  Lv. {elemental.level} {elemental.nickname} "
                f"`{HealthBarView.from_elemental(elemental)} "
                f"{elemental.current_hp} / {elemental.max_hp} HP` \n")

    async def pick_option(self, reaction: str) -> None:
        await super().pick_option(reaction)
        if self._selected_value is not None:
            await self.create_detail_view(self._selected_value)

    async def create_detail_view(self, elemental: Elemental) -> None:
        form = StatusDetailView(self.bot,
                                self.player,
                                elemental,
                                self.discord_message)
        await form.render()
        self.player.set_primary_view(form)


class StatusDetailView(Form):
    """
    A detail view for an Elemental on your team.
    """
    def __init__(self,
                 bot,
                 player,
                 elemental,
                 message=None):
        super().__init__(bot)
        self.player = player
        self.elemental = elemental
        # No button values here. Customized emojis will trigger different operations.
        self.discord_message = message

    @property
    def buttons(self) -> List[Form.Button]:
        buttons = ['🔙', '⚔', '💪', '🏷', '📝']
        return [Form.Button(button, None) for button in buttons]

    async def render(self) -> None:
        if not self.discord_message:
            self.discord_message = await self.bot.say(self.get_status())
        else:
            await self.bot.edit_message(self.discord_message, self.get_status())
        await self.bot.clear_reactions(self.discord_message)
        for button in self.buttons:
            await self.bot.add_reaction(self.discord_message, button.reaction)

    def get_status(self) -> str:
        # Renders HP, EXP, stats and currently active abilities and traits.
        elemental = self.elemental
        view = (f"{elemental.left_icon} {self.get_name()} "
                f"Lv. {elemental.level} (EXP: {elemental.current_exp} / {elemental.exp_to_level})\n"
                f"`{HealthBarView.from_elemental(elemental)} {elemental.current_hp} / {elemental.max_hp} HP`\n"
                f"{StatsView(elemental).get_view()}")
        note = f"Note: {elemental.note}" if elemental.note else ''
        option_descriptions = f"[⚔ Abilities]   [💪 Attributes]   [🏷 Nickname]   [📝 Note]"
        return '\n'.join([view, note, option_descriptions])

    def get_name(self) -> str:
        # If the Elemental has a nickname, also display its actual species name.
        name = self.elemental.name
        nickname = self.elemental.nickname
        if nickname != name:
            return f"**{nickname}** [{name}]"
        return f"**{name}**"

    async def back(self):
        """
        Rerenders the Status form.
        """
        form = StatusView(self.bot,
                          self.player)
        await form.render()
        self.player.set_primary_view(form)