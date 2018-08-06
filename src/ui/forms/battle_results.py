from typing import List

from src.core.constants import FIGHT, STATUS
from src.ui.forms.form import Form


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
        await self._add_reactions([FIGHT, STATUS])

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
        enemy_names = ', '.join([team.owner for team in enemy_side if team.owner is not None])
        if enemy_names:
            view.append(f'You won against {enemy_names}.')

    def _render_defeat(self, view: List[str]) -> None:
        view.append('```--- Defeat ---```')
        enemy_side = self.combat.get_enemy_side(self.combat_team)
        enemy_names = ', '.join([team.owner for team in enemy_side if team.owner is not None])
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

    def pick_option(self, reaction: str) -> bool:
        pass