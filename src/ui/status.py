from src.elemental.elemental import Elemental
from src.ui.form import Form
from src.ui.health_bar import HealthBarView
from src.ui.stats import StatsView


class Status(Form):
    """
    Shows the status of your team.
    """
    def __init__(self,
                 bot,
                 player):
        super().__init__(bot)
        self.player = player
        self.options = self.player.team.elementals
        self.buttons = Form.static_options()[:player.team.size]

    async def render(self) -> None:
        message_body = f"```{self.player.nickname}'s Team ({self.player.team.size}/4)```"
        for i, elemental in enumerate(self.options):
            message_body += self._get_status(i, elemental)
        self.message = await self.bot.say(message_body)
        for button in self.buttons:
            await self.bot.add_reaction(self.message, button)

    @staticmethod
    def _get_status(index: int, elemental: Elemental) -> str:
        return (f"{index + 1}) {elemental.left_icon}  Lv. {elemental.level} {elemental.nickname} "
                f"`{HealthBarView.from_elemental(elemental)} "
                f"{elemental.current_hp} / {elemental.max_hp} HP` \n")

    async def pick_option(self, reaction: str) -> None:
        await super().pick_option(reaction)
        if self._selected_index is not None:
            await self.create_detail_view(self.options[self._selected_index])

    async def create_detail_view(self, elemental: Elemental) -> None:
        form = DetailStatus(self.bot, self.player, elemental)
        form.set_message(self.message)
        await form.render()
        self.player.current_view = form

    async def _confirm(self):
        # No operation.
        pass


class DetailStatus(Form):
    """
    A detail view for an Elemental on your team.
    """

    def __init__(self,
                 bot,
                 player,
                 elemental):
        super().__init__(bot)
        self.player = player
        self.elemental = elemental
        self.buttons = ['🔙', '⚔', '💪', '✏', '📝']

    def set_message(self, message) -> None:
        self.message = message

    async def render(self) -> None:
        if not self.message:
            self.message = await self.bot.say(self.get_status())
        else:
            await self.bot.edit_message(self.message, self.get_status())
        await self.bot.clear_reactions(self.message)
        for button in self.buttons:
            await self.bot.add_reaction(self.message, button)

    def get_status(self) -> str:
        # Renders HP, EXP, stats and currently active abilities and traits.
        elemental = self.elemental
        view = (f"{elemental.left_icon} {self.get_name()} "
                f"Lv. {elemental.level} (EXP: {elemental.current_exp} / {elemental.exp_to_level})\n"
                f"`{HealthBarView.from_elemental(elemental)} {elemental.current_hp} / {elemental.max_hp} HP`\n"
                f"*{elemental.description}*\n\n"
                f"{StatsView(elemental).get_view()}")
        note = f"Note: {elemental.note}" if elemental.note else ''
        option_descriptions = f"[⚔ Abilities] [💪 Attributes] [✏ Nickname] [📝 Note]"
        return '\n'.join([view, note, option_descriptions])

    def get_name(self) -> str:
        # If the Elemental has a nickname, also display its actual species name.
        name = self.elemental.name
        nickname = self.elemental.nickname
        if nickname != name:
            return f"**{nickname}** [{name}]"
        return f"**{name}**"

    def _confirm(self):
        # No operation.
        pass

    def back(self):
        """
        Rerenders the Status form.
        """
        pass