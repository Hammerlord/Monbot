from src.elemental.elemental import Elemental
from src.ui.form import Form
from src.ui.health_bar import HealthBarView


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
        return (f"{index + 1}) {elemental.left_icon} {elemental.nickname} "
                f"`{HealthBarView.from_elemental(elemental)} "
                f"{elemental.current_hp} / {elemental.max_hp} HP` \n")

    async def confirm(self):
        # No operation.
        pass
