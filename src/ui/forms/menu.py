from src.combat.battle_manager import BattleManager
from src.core.constants import STATUS, BAG, FIGHT, MAP, SHOP, VS, SUMMON, CRAFT
from src.data.data_manager import DataManager
from src.shop.general_shop import GeneralShop
from src.ui.forms.battle import BattleViewOptions, BattleView
from src.ui.forms.form import Form, FormOptions, ValueForm
from src.ui.forms.status import StatusView
from src.ui.view_router import ViewRouter


class MainMenu(Form):
    """
    Shows all the menu options available to a player.
    """

    def __init__(self, options: FormOptions):
        super().__init__(options)
        self.router = ViewRouter(options.bot)

    async def render(self) -> None:
        view = '\n'.join([self._main_view, self._options])
        self._display(view)
        await self._add_reactions([STATUS, FIGHT, SUMMON, SHOP, VS])

    @property
    def _main_view(self) -> str:
        return '\n'.join([f"```{self.player.nickname}'s status",
                          f"Level {self.player.level}   "
                          f"({self.player.current_exp}/{self.player.exp_to_level} EXP)```"])

    @property
    def _options(self) -> str:
        return '   '.join([f"{STATUS} `Team Status`",
                           f"{FIGHT} `Battle`",
                           # f"{MAP} `Travel`",
                           # f"{CRAFT} `Craft`",
                           f"{SUMMON} `Summon`",
                           f"{SHOP} `Shop`",
                           f"{VS} `PVP`"])

    async def pick_option(self, reaction: str) -> None:
        if reaction == STATUS:
            await self.router.show_status(self.player)
        elif reaction == FIGHT and self.player.can_battle:
            combat_team = BattleManager().create_pve_combat(self.player)
            await self.router.show_battle(self.player, combat_team)
        elif reaction == MAP:
            pass
        elif reaction == CRAFT:
            pass
        elif reaction == SUMMON:
            await self.router.show_summon(self.player, DataManager())
        elif reaction == SHOP:
            await self.router.show_shop(GeneralShop(), self.player)
        elif reaction == VS and self.discord_message.server:
            await self.router.show_versus(self.player, DataManager(), self.discord_message.server)


