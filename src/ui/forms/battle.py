from typing import List

import discord
from discord.ext.commands import Bot

from src.character.player import Player
from src.combat.combat import Combat
from src.core.constants import *
from src.team.combat_team import CombatTeam
from src.ui.forms.form import FormOptions, Form, ValueForm
from src.ui.health_bar import HealthBarView


class BattleViewOptions(FormOptions):
    """
    The dependencies of BattleView.
    """
    def __init__(self,
                 bot: Bot,
                 player: Player,
                 combat: Combat,
                 combat_team: CombatTeam,
                 discord_message: discord.Message = None):
        super().__init__(bot, player, discord_message)
        self.combat = combat
        self.combat_team = combat_team


class BattleView(Form):
    """
    A navigation view showing the battle from one team's perspective.
    TODO doesn't support multiple teams on the same side.
    Has a number of subviews, including: selecting Ability, selecting Elemental, selecting Item
    """
    def __init__(self, options: BattleViewOptions):
        super().__init__(options)
        self.combat = options.combat
        self.combat_team = options.combat_team

    def get_main_view(self) -> str:
        return self.get_battlefield()

    def get_battlefield(self) -> str:
        opponent = self.combat.get_active_enemy(self.combat_team.active_elemental)
        elemental = self.combat_team.active_elemental
        return (f"{opponent.nickname} Lv. {opponent.level}\n"
                f"{HealthBarView.from_elemental(opponent)} ({opponent.health_percent}%)  {opponent.icon}\n"
                f"{elemental.icon}   {elemental.nickname} Lv. {elemental.level}\n"
                f"       {HealthBarView.from_elemental(elemental)}")

    async def render(self):
        await self._display(self.get_main_view())
        await self._clear_reactions()
        for reaction in [ABILITIES, RETURN]:
            await self.bot.add_reaction(self.discord_message, reaction)
        if self.combat.allow_items:
            await self.bot.add_reaction(self.discord_message, ITEM)
        if self.combat.allow_flee:
            await self.bot.add_reaction(self.discord_message, FLEE)

    def pick_option(self, reaction: str) -> None:
        if reaction == ABILITIES:
            pass
        elif reaction == RETURN:
            pass
        elif reaction == ITEM and self.combat.allow_items:
            pass
        elif reaction == FLEE and self.combat.allow_flee:
            pass


class SelectElementalView(ValueForm):

    @property
    def buttons(self) -> List[ValueForm.Button]:
        pass

    @property
    def values(self) -> List[any]:
        pass

    def render(self) -> None:
        pass


class SelectAbilityView(ValueForm):

    @property
    def buttons(self) -> List[ValueForm.Button]:
        pass

    @property
    def values(self) -> List[any]:
        pass

    def render(self) -> None:
        pass