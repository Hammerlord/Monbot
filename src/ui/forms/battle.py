import asyncio
from typing import List

import discord
from discord.ext.commands import Bot

from src.character.inventory import ItemSlot, Item
from src.character.player import Player
from src.combat.actions.action import EventLog
from src.combat.battle_manager import BattleManager
from src.combat.combat import Combat
from src.core.constants import *
from src.elemental.combat_elemental import CombatElemental
from src.team.combat_team import CombatTeam
from src.ui.ability_option import AbilityOptionView
from src.ui.battlefield import Battlefield
from src.ui.forms.form import FormOptions, Form, ValueForm
from src.ui.forms.status import StatusView
from src.ui.health_bar import HealthBarView


class BattleViewOptions(FormOptions):
    """
    The dependencies of BattleView.
    """

    def __init__(self,
                 bot: Bot,
                 player: Player,
                 combat_team: CombatTeam,
                 discord_message: discord.Message = None,
                 previous_form: 'BattleView' or Form = None):
        super().__init__(bot, player, discord_message, previous_form)
        self.combat_team = combat_team


class BattleView(Form):
    """
    A navigation view showing the battle from one team's perspective.
    TODO doesn't support multiple teams on the same side.
    Has a number of subviews, including: selecting Ability, selecting Elemental, selecting Item
    """

    def __init__(self, options: BattleViewOptions):
        super().__init__(options)
        self.combat_team = options.combat_team
        self.combat = options.combat_team.combat
        self.logger = self.combat.turn_logger
        self.log_index = self.logger.most_recent_index

    async def render(self) -> None:
        # TODO it is possible to have no available options, in which case, we need a skip.
        await self._clear_reactions()
        await self._render_main()

    async def rerender(self) -> None:
        """
        Show this screen again after making a move.
        """
        self.player.set_primary_view(self)
        await self._clear_reactions()
        await self._render_battle_recaps()
        await self._render_main()

    async def _render_main(self) -> None:
        if not self.combat.in_progress:
            await asyncio.sleep(1.0)
            await Form.from_form(self, BattleResults)
            return
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
        self.log_index = self.logger.most_recent_index

    async def _render_current(self) -> None:
        """
        Render the current state of the battlefield and options, if available.
        """
        side_a = self.combat.side_a_active
        side_b = self.combat.side_b_active
        allies = side_a if self.combat_team.side == Combat.SIDE_A else side_b
        opponents = side_b if allies == side_a else side_a
        battlefield = Battlefield(allies, opponents).get_view()
        view = f"{battlefield}{self._display_options()}"
        await self._display(view)

    async def _render_events(self, turn_log: List[EventLog]) -> None:
        """
        Show everything that happened during a given turn.
        """
        for log in turn_log:
            if not log.side_a or not log.side_b:
                continue
            allies = log.side_a if self.combat_team.side == Combat.SIDE_A else log.side_b
            opponents = log.side_b if allies == log.side_a else log.side_a
            battlefield = Battlefield(allies, opponents).get_view()
            is_enemy_action = log.acting_team.side != self.combat_team.side
            recap = f"{'<Enemy> ' if is_enemy_action else ''}{log.recap}"
            message = ''.join([battlefield, f'```{recap}```'])
            await self._display(message)
            await asyncio.sleep(1.5)

    async def check_add_options(self) -> None:
        if not self.combat.in_progress:
            return
        await self._add_reaction(ABILITIES)
        if self.combat_team.eligible_bench:
            await self._add_reaction(SWITCH)
        if self.combat.allow_items and self.player.consumables:
            await self._add_reaction(MEAT)
        if self.combat.allow_flee:
            await self._add_reaction(FLEE)

    def _display_options(self) -> str:
        if not self.combat.in_progress:
            return ''
        options = [f"{ABILITIES} `Abilities`"]
        if self.combat_team.eligible_bench:
            options.append(f"{SWITCH} `Switch`")
        if self.combat.allow_items and self.player.consumables:
            options.append(f"{MEAT} `Items`")
        if self.combat.allow_flee:
            options.append(f"{FLEE} `Flee`")
        return ' '.join(options)

    def get_form_options(self) -> BattleViewOptions:
        return BattleViewOptions(self.bot,
                                 self.player,
                                 self.combat,
                                 self.combat_team,
                                 self.discord_message,
                                 previous_form=self)

    async def pick_option(self, reaction: str) -> None:
        if not self.combat.in_progress:
            return
        if reaction == ABILITIES:
            await Form.from_form(self, SelectAbilityView)
        elif reaction == SWITCH and self.combat_team.eligible_bench:
            await Form.from_form(self, SelectElementalView)
        elif reaction == MEAT and self.combat.allow_items and self.player.consumables:
            await Form.from_form(self, SelectConsumableView)
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
    def values(self) -> List[CombatElemental]:
        return self.combat_team.eligible_bench

    async def render(self) -> None:
        await self._display(self.get_team())
        await self._clear_reactions()
        for button in self.buttons:
            await self._add_reaction(button.reaction)
        await self._add_reaction(BACK)

    def get_team(self) -> str:
        message_body = f"```{self.player.nickname}'s team```"
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
        index = str(index + 1) + ') ' if index is not None else ''
        return (f"{index}{elemental.icon}  Lv. {elemental.level} {elemental.nickname}  "
                f"`{HealthBarView.from_elemental(elemental)} "
                f"{elemental.current_hp}/{elemental.max_hp} HP` "
                f"{MANA} `{elemental.current_mana}/{elemental.max_mana}`\n")

    async def pick_option(self, reaction: str) -> None:
        if reaction == BACK:
            await self._back()
            return
        await super().pick_option(reaction)
        if self.toggled:
            self.combat_team.attempt_switch(self._selected_value)
            await self.previous_form.rerender()


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
        side_a = self.combat.side_a_active
        side_b = self.combat.side_b_active
        allies = side_a if self.combat_team.side == Combat.SIDE_A else side_b
        opponents = side_b if allies == side_a else side_a
        return Battlefield(allies,
                           opponents).get_view()

    def get_abilities(self) -> str:
        """
        :return: A string showing enumerated available abilities.
        """
        elemental = self.combat_team.active_elemental
        ability_views = []
        for i, ability in enumerate(elemental.available_abilities):
            ability_views.append(f'{ValueForm.ENUMERATED_REACTIONS[i]} {AbilityOptionView(ability).get_summary()}')
        return '\n'.join(ability_views)

    def get_main_view(self) -> str:
        return ''.join([self.get_battlefield(), self.get_abilities()])

    async def render(self) -> None:
        await self._display(self.get_main_view())
        await self._clear_reactions()
        for button in self.buttons:
            await self._add_reaction(button.reaction)
        await self._add_reaction(BACK)

    async def pick_option(self, reaction: str):
        if reaction == BACK:
            # TODO this is broken.
            await self._back()
            return
        await super().pick_option(reaction)
        if self.toggled:
            self.combat_team.select_ability(self._selected_value)
            await self.previous_form.rerender()


class SelectConsumableView(ValueForm):
    """
    Displays items eligible for use in combat. You can only use one at a time,
    which submits an Action request to the battle.
    """

    def __init__(self, options: BattleViewOptions):
        super().__init__(options)
        self.combat = options.combat
        self.combat_team = options.combat_team

    @property
    def values(self) -> List[ItemSlot]:
        return self.player.consumables

    @property
    def buttons(self) -> List[ValueForm.Button]:
        return [ValueForm.Button(item_slot.item.icon, item_slot.item) for item_slot in self.values]

    async def render(self) -> None:
        await self._clear_reactions()
        await self._display(self._view)
        for button in self.buttons:
            await self._add_reaction(button.reaction)
        await self._add_reaction(BACK)

    @property
    def _view(self) -> str:
        return f"```Usable items``` " f"{self._item_views}"

    @property
    def _item_views(self) -> str:
        return '\n'.join([f"{slot.item.icon} **{slot.item.name} x{slot.amount}** {slot.item.properties}"
                          for slot in self.values])

    async def pick_option(self, reaction: str) -> None:
        if reaction == BACK:
            await self._back()
            return
        await super().pick_option(reaction)
        item = self._selected_value
        if item is not None:
            options = UseConsumableOptions(self.bot,
                                           self.player,
                                           item,
                                           self.combat_team,
                                           battle_view=self.previous_form,
                                           discord_message=self.discord_message,
                                           previous_form=self)
            form = UseConsumableView(options)
            await form.show()


class UseConsumableOptions(FormOptions):
    """
    Dependencies of in-combat UseConsumableView.
    """

    def __init__(self,
                 bot: Bot,
                 player: Player,
                 item: Item,
                 combat_team: CombatTeam,
                 battle_view: BattleView,
                 discord_message: discord.Message,
                 previous_form: Form):
        super().__init__(bot, player, discord_message, previous_form)
        self.combat_team = combat_team
        self.battle_view = battle_view
        self.item = item


class UseConsumableView(ValueForm):
    def __init__(self, options: UseConsumableOptions):
        super().__init__(options)
        self.item = options.item
        self.combat_team = options.combat_team
        self.battle_view = options.battle_view

    @property
    def values(self) -> List[any]:
        return [elemental for elemental in self.combat_team.elementals if self.item.is_usable_on(elemental)]

    @property
    def buttons(self) -> List[ValueForm.Button]:
        return ValueForm.enumerated_buttons(self.values)

    async def render(self) -> None:
        await self._display(self._view)
        await self._clear_reactions()
        for button in self.buttons:
            await self._add_reaction(button.reaction)
        await self._add_reaction(BACK)

    @property
    def _view(self) -> str:
        items_left = self.player.inventory.amount_left(self.item)
        return (f"Selected **{self.item.icon} {self.item.name} ({items_left} left)** \n"
                f"{self.item.properties} \n {self._eligible_elementals}")

    @property
    def _eligible_elementals(self) -> str:
        if len(self.values) == 0:
            return "```(You don't have anyone to use this item on.)```"
        message_body = '\n'.join([self._get_status(elemental, i) for i, elemental in enumerate(self.values)])
        message_body += f"```Give {self.item.name} to who?```"
        return message_body

    @staticmethod
    def _get_status(elemental: CombatElemental, index=None) -> str:
        index = ValueForm.ENUMERATED_REACTIONS[index] if index is not None else ''
        return (f"{index} {elemental.icon}  Lv. {elemental.level} {elemental.nickname}  "
                f"`{HealthBarView.from_elemental(elemental)} "
                f"{elemental.current_hp} / {elemental.max_hp} HP` \n")

    async def pick_option(self, reaction: str) -> None:
        if reaction == BACK:
            await self._back()
            return
        await super().pick_option(reaction)
        elemental = self._selected_value
        if self.toggled:
            self.combat_team.use_item(self.item, elemental)
            await self.battle_view.rerender()


class BattleResults(Form):
    """
    Shows the results of a battle after it ends.
    Presents options to keep fighting or view status.
    """

    def __init__(self, options):
        """
        :param options: BattleViewOptions
        """
        super().__init__(options)
        self.combat = options.combat
        self.combat_team = options.combat_team

    async def render(self) -> None:
        await self._display(self._view)
        await self._clear_reactions()
        if self.player.can_battle:
            await self._add_reaction(FIGHT)
        await self._add_reaction(STATUS)

    @property
    def _view(self) -> str:
        view = []
        if self.combat.winning_side is None:
            view.append('```--- Tie ---```')
        elif self.combat_team in self.combat.winning_side:
            self._render_victory(view)
        else:
            self._render_defeat(view)
        view.append(f'Earned {self.combat_team.exp_earned} EXP.')
        self._render_loot(view)
        view.append(f"\n {self._display_options}")
        return '\n'.join(view)

    @property
    def _display_options(self) -> str:
        return '  '.join([f'{FIGHT} `Next Battle`', f'{STATUS} `Status`'])

    def _render_victory(self, view: List[str]) -> None:
        enemy_side = self.combat.get_enemy_side(self.combat_team)
        view.append('```--- Victory! ---```')
        enemy_names = ', '.join([team.owner.nickname for team in enemy_side if team.owner is not None])
        if enemy_names:
            view.append(f'You won against {enemy_names}.')

    def _render_defeat(self, view: List[str]) -> None:
        view.append('```--- Defeat ---```')
        enemy_side = self.combat.get_enemy_side(self.combat_team)
        enemy_names = ', '.join([team.owner.nickname for team in enemy_side if team.owner is not None])
        if enemy_names:
            view.append(f'You lost against {enemy_names}.')

    def _render_loot(self, view: List[str]) -> None:
        if self.combat_team.gold_earned > 0:
            view.append(f"Received {self.combat_team.gold_earned} gold.")
        if not self.combat_team.items_earned:
            return
        view.append("Obtained:")
        for item_slot in self.combat_team.items_earned:
            item = item_slot.item
            view.append(f"{item.icon} {item.name} x{item_slot.amount}")

    async def pick_option(self, reaction: str) -> None:
        if self.player.can_battle and reaction == FIGHT:
            combat_team = BattleManager().create_pve_combat(self.player)
            view_options = BattleViewOptions(
                self.bot,
                self.player,
                combat_team=combat_team,
                discord_message=self.discord_message
            )
            await BattleView(view_options).show()
        elif reaction == STATUS:
            options = FormOptions(self.bot, self.player, self.discord_message)
            await StatusView(options).show()
