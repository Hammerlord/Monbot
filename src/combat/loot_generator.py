from typing import List

from src.items.loot import roll_loot
from src.team.combat_team import CombatTeam


class LootGenerator:
    def __init__(self,
                 winning_side: List[CombatTeam],
                 losing_side: List[CombatTeam]):
        """
        :param winning_side: The teams to grant loot and money to.
        :param losing_side: The teams to generate loot and money from.
        """
        self.winning_side = winning_side
        self.losing_side = losing_side
        self.gold_earned = 0  # TODO no need to store it here?
        self.items_dropped = []

    def generate_loot(self) -> None:
        self.gold_earned = self._calculate_gold_earned()
        self.items_dropped = self._roll_items_dropped()
        for team in self.winning_side:
            team.add_gold(self.gold_earned)
            team.add_items(self.items_dropped)  # TODO unique rolls for everyone?

    def _roll_items_dropped(self):
        """
        Only wild Elementals drop loot.
        :return: List[Item]
        """
        items = []
        for team in self.losing_side:
            if team.owner is not None:
                continue
            for elemental in team.elementals:
                items += roll_loot(elemental)
        return items

    def _calculate_gold_earned(self) -> int:
        """
        Calculate gold based on the losing side, if their teams have an owner (and therefore money).
        Note this doesn't actually deduct any gold.
        """
        gold = 0
        for team in self.losing_side:
            if team.owner:
                gold += team.owner.level + 5
        return gold
