import discord
from discord.ext.commands import Bot

from src.combat.battle_manager import BattleManager
from src.core.constants import *
from src.data.data_manager import DataManager
from src.shop.general_shop import GeneralShop
from src.ui.forms.battle import BattleViewOptions, BattleView
from src.ui.forms.form import FormOptions, Form
from src.ui.forms.shop import ShopViewOptions, ShopView
from src.ui.forms.status import StatusView
from src.ui.forms.summon import SummonMenuOptions, SummonMenu
from src.ui.forms.versus import VersusFormOptions, VersusForm


class MainMenu(Form):
    """
    Shows all the menu options available to a player.
    """

    def __init__(self, options: FormOptions):
        super().__init__(options)

    async def render(self) -> None:
        await self._clear_reactions()
        view = '\n'.join([self._main_view, self._options])
        await self._display(view)
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
            await self._show_status()
        elif reaction == FIGHT and self.player.can_battle:
            await self._show_fight()
        elif reaction == MAP:
            pass
        elif reaction == CRAFT:
            pass
        elif reaction == SUMMON:
            await self._show_summon()
        elif reaction == SHOP:
            await self._show_shop()
        elif reaction == VS and self.discord_message.server:
            await self._show_versus()

    async def _show_status(self) -> None:
        options = FormOptions(self.bot,
                              self.player,
                              self.discord_message,
                              self)
        await StatusView(options).show()

    async def _show_fight(self) -> None:
        combat_team = BattleManager().create_pve_combat(self.player)
        options = BattleViewOptions(self.bot,
                                    self.player,
                                    combat_team,
                                    self.discord_message)
        await BattleView(options).show()

    async def _show_summon(self) -> None:
        options = SummonMenuOptions(self.bot,
                                    self.player,
                                    DataManager(),
                                    self.discord_message,
                                    self)
        await SummonMenu(options).show()

    async def _show_shop(self) -> None:
        options = ShopViewOptions(self.bot,
                                  self.player,
                                  GeneralShop(),
                                  self.discord_message,
                                  self)
        await ShopView(options).show()

    async def _show_versus(self) -> None:
        options = VersusFormOptions(self.bot,
                                    self.player,
                                    DataManager(),
                                    self.discord_message.server,
                                    self.discord_message,
                                    self)
        await VersusForm(options).show()
