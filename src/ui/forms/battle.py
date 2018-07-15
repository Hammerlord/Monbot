from typing import List

import discord
from discord.ext.commands import Bot

from src.character.player import Player
from src.combat.combat import Combat
from src.combat.combat_actions import ActionType
from src.core.constants import *
from src.team.combat_team import CombatTeam
from src.ui.ability_option import AbilityOptionView
from src.ui.battlefield import Battlefield
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

    def get_last_actions(self) -> str:
        # If a switch is involved, always render the player's switch first.
        if self.combat_team.last_action.action_type == ActionType.SWITCH:
            pass  # TODO

    def get_battlefield(self) -> str:
        return Battlefield(self.combat_team.active_elemental,
                           self.combat_team.get_active_enemy()).get_view()

    async def render(self):
        # TODO it is possible to have no available options, in which case, we need a skip.
        await self._display(self.get_main_view())
        await self._clear_reactions()
        await self.bot.add_reaction(self.discord_message, ABILITIES)
        if self.combat_team.eligible_bench:
            await self.bot.add_reaction(self.discord_message, RETURN)
        if self.combat.allow_items:
            await self.bot.add_reaction(self.discord_message, ITEM)
        if self.combat.allow_flee:
            await self.bot.add_reaction(self.discord_message, FLEE)

    def get_form_options(self) -> BattleViewOptions:
        return BattleViewOptions(self.bot,
                                 self.player,
                                 self.combat,
                                 self.combat_team,
                                 self.discord_message)

    async def pick_option(self, reaction: str) -> None:
        if reaction == ABILITIES:
            await Form.from_form(self, SelectAbilityView)
        elif reaction == RETURN and self.combat_team.eligible_bench:
            await Form.from_form(self, SelectElementalView)
        elif reaction == ITEM and self.combat.allow_items:
            pass
        elif reaction == FLEE and self.combat.allow_flee:
            pass


class SelectElementalView(ValueForm):
    """
    Displays your benched CombatElementals, and allows you to switch one in.
    """

    def __init__(self, options: BattleViewOptions):
        super().__init__(options)
        self.combat = options.combat
        self.combat_team = options.combat_team

    @property
    def buttons(self) -> List[ValueForm.Button]:
        return ValueForm.enumerated_buttons(self.values)

    @property
    def values(self) -> List[any]:
        return self.combat_team.eligible_bench

    async def render(self) -> None:
        await self._clear_reactions()
        for button in self.buttons:
            await self.bot.add_reaction(self.discord_message, button.reaction)

    async def pick_option(self, reaction: str) -> None:
        await super().pick_option(reaction)
        if self.toggled:
            self.combat_team.attempt_switch(self._selected_value)
            await Form.from_form(self, BattleView)

    def get_form_options(self) -> BattleViewOptions:
        return BattleViewOptions(self.bot,
                                 self.player,
                                 self.combat,
                                 self.combat_team,
                                 self.discord_message)


class SelectAbilityView(ValueForm):
    """
    Displays your currently active CombatElemental's active abilities.
    """

    def __init__(self, options: BattleViewOptions):
        super().__init__(options)
        self.combat = options.combat
        self.combat_team = options.combat_team

    @property
    def buttons(self) -> List[ValueForm.Button]:
        return ValueForm.enumerated_buttons(self.values)

    @property
    def values(self) -> List[any]:
        return self.combat_team.active_elemental.abilities

    def get_battlefield(self) -> str:
        return Battlefield(self.combat_team.active_elemental,
                           self.combat_team.get_active_enemy()).get_view()

    def get_abilities(self) -> str:
        """
        :return: A string showing enumerated available abilities.
        """
        elemental = self.combat_team.active_elemental
        ability_views = []
        for i, ability in enumerate(elemental.available_abilities):
            ability_views.append(f'{i + 1}) {AbilityOptionView(ability).get_detail()}')
        return '\n'.join(ability_views)

    def get_main_view(self) -> str:
        return '\n'.join([self.get_battlefield(), self.get_abilities()])

    async def render(self) -> None:
        await self._display(self.get_main_view())
        await self._clear_reactions()
        for button in self.buttons:
            await self.bot.add_reaction(self.discord_message, button.reaction)

    async def pick_option(self, reaction: str):
        await super().pick_option(reaction)
        if self.toggled:
            self.combat_team.select_ability(self._selected_value)
            await Form.from_form(self, BattleView)

    def get_form_options(self) -> BattleViewOptions:
        return BattleViewOptions(self.bot,
                                 self.player,
                                 self.combat,
                                 self.combat_team,
                                 self.discord_message)
