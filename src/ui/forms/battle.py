import asyncio
from typing import List

import discord
from discord.ext.commands import Bot

from src.character.player import Player
from src.combat.actions.action import EventLog
from src.combat.combat import Combat
from src.core.constants import *
from src.elemental.combat_elemental import CombatElemental
from src.elemental.elemental import Elemental
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

    def __init__(self, options: BattleViewOptions, recap_turn=False):
        """
        :param recap_turn: Should we replay events from the last turn(s)?
        """
        super().__init__(options)
        self.combat = options.combat
        self.combat_team = options.combat_team
        self.recap_turn = recap_turn
        self.logger = self.combat.turn_logger
        self.log_index = self.logger.most_recent_index

    async def render(self) -> None:
        # TODO it is possible to have no available options, in which case, we need a skip.
        await self._clear_reactions()
        if self.recap_turn:
            await self._render_battle_recaps()
        await self._render_current()
        if self.combat_team.active_elemental.is_knocked_out and self.combat_team.eligible_bench:
            # Render the mon selection view if your mon has been knocked out and you have another.
            await asyncio.sleep(1.0)
            await Form.from_form(self, SelectElementalView)
        else:
            await self.check_add_options()

    async def _render_battle_recaps(self) -> None:
        """
        Render the turn(s) that occurred since we last updated the view.
        """
        turn_logs = self.logger.get_turn_logs(self.log_index)
        for turn_log in turn_logs:
            await self._render_events(turn_log)

    async def _render_current(self) -> None:
        battlefield = Battlefield(self.combat.side_a_active,
                                  self.combat.side_b_active,
                                  self.combat_team).get_view()
        await self._display(battlefield)

    async def _render_events(self, turn_log: List[EventLog]) -> None:
        """
        Show everything that happened during a given turn.
        """
        for log in turn_log:
            if not log.side_a or not log.side_b:
                continue
            battlefield = Battlefield(log.side_a,
                                      log.side_b,
                                      self.combat_team).get_view()
            recap = log.recap  # TODO enemy recaps
            message = '\n'.join([battlefield, f'```{recap}```'])
            await self._display(message)
            await asyncio.sleep(1.5)

    async def check_add_options(self) -> None:
        if not self.combat.in_progress:
            return
        await self._add_reaction(ABILITIES)
        if self.combat_team.eligible_bench:
            await self._add_reaction(RETURN)
        if self.combat.allow_items:
            await self._add_reaction(ITEM)
        if self.combat.allow_flee:
            await self._add_reaction(FLEE)

    def get_form_options(self) -> BattleViewOptions:
        return BattleViewOptions(self.bot,
                                 self.player,
                                 self.combat,
                                 self.combat_team,
                                 self.discord_message)

    async def pick_option(self, reaction: str) -> None:
        if not self.combat.in_progress:
            return
        if reaction == ABILITIES:
            await Form.from_form(self, SelectAbilityView)
        elif reaction == RETURN and self.combat_team.eligible_bench:
            await Form.from_form(self, SelectElementalView)
        elif reaction == ITEM and self.combat.allow_items:
            pass
        elif reaction == FLEE and self.combat.allow_flee:
            pass

    @staticmethod
    async def from_form(from_form, recap_turn=False):
        options = from_form.get_form_options()
        new_form = BattleView(options, recap_turn)
        options.player.set_primary_view(new_form)
        await new_form.render()


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
    def values(self) -> List[CombatElemental]:
        return self.combat_team.eligible_bench

    async def render(self) -> None:
        await self._display(self.get_team())
        await self._clear_reactions()
        for button in self.buttons:
            await self._add_reaction(button.reaction)
        await self._add_reaction(BACK)

    def get_team(self) -> str:
        message_body = f"```{self.player.nickname}'s Team```"
        message_body += f'**Active:** {self._get_status(self.combat_team.active_elemental)}\n'
        for i, elemental in enumerate(self.values):
            message_body += self._get_status(elemental, i)
        knocked_out_elementals = self.combat_team.get_knocked_out
        if knocked_out_elementals:
            message_body += '\n--Knocked Out--\n'
            for elemental in knocked_out_elementals:
                message_body += self._get_status(elemental)
        message_body += '```Select an Elemental to switch.```'
        return message_body

    @staticmethod
    def _get_status(elemental: CombatElemental, index=None) -> str:
        index = str(index + 1) + ')' if index is not None else ''
        return (f"{index} {elemental.icon}  Lv. {elemental.level} {elemental.nickname}  "
                f"`{HealthBarView.from_elemental(elemental)} "
                f"{elemental.current_hp} / {elemental.max_hp} HP` \n")

    async def pick_option(self, reaction: str) -> None:
        if reaction == BACK:
            await self.back()
            return
        await super().pick_option(reaction)
        if self.toggled:
            self.combat_team.attempt_switch(self._selected_value)
            await BattleView.from_form(self, recap_turn=True)

    async def back(self) -> None:
        """
        Rerenders the Battle view.
        """
        await BattleView.from_form(self)

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
        return self.combat_team.active_elemental.available_abilities

    def get_battlefield(self) -> str:
        return Battlefield(self.combat.side_a_active,
                           self.combat.side_b_active,
                           self.combat_team).get_view()

    def get_abilities(self) -> str:
        """
        :return: A string showing enumerated available abilities.
        """
        elemental = self.combat_team.active_elemental
        ability_views = []
        for i, ability in enumerate(elemental.available_abilities):
            ability_views.append(f'{i + 1}) {AbilityOptionView(ability).get_summary()}')
        return '\n'.join(ability_views)

    def get_main_view(self) -> str:
        return '\n'.join([self.get_battlefield(), self.get_abilities()])

    async def render(self) -> None:
        await self._display(self.get_main_view())
        await self._clear_reactions()
        for button in self.buttons:
            await self._add_reaction(button.reaction)
        await self._add_reaction(BACK)

    async def pick_option(self, reaction: str):
        if reaction == BACK:
            await self.back()
            return
        await super().pick_option(reaction)
        if self.toggled:
            self.combat_team.select_ability(self._selected_value)
            await BattleView.from_form(self, recap_turn=True)

    async def back(self) -> None:
        """
        Rerenders the Battle view.
        """
        await BattleView.from_form(self)

    def get_form_options(self) -> BattleViewOptions:
        return BattleViewOptions(self.bot,
                                 self.player,
                                 self.combat,
                                 self.combat_team,
                                 self.discord_message)
