from random import randint
from typing import List

from src.core.elements import Effectiveness
from src.team.combat_team import CombatTeam


class CombatAI:
    """
    An AI controller for a CombatTeam that selects Abilities and decides when to switch.
    """
    def __init__(self,
                 combat_team: CombatTeam):
        self.team = combat_team

    def pick_move(self) -> None:
        if self.team.active_elemental.is_knocked_out and self.team.eligible_bench:
            self.switch()
        else:
            self.pick_ability()

    def switch(self) -> None:
        effective_elementals = Effectiveness.find_effective(self.team.eligible_bench,
                                                            self.team.get_active_enemy().element)
        if effective_elementals:
            self.team.attempt_switch(effective_elementals[0])
            return

        neutral_elementals = Effectiveness.find_neutral(self.team.eligible_bench,
                                                        self.team.get_active_enemy().element)
        if neutral_elementals:
            self.team.attempt_switch(neutral_elementals[0])
            return

        self.team.attempt_switch(self.roll(self.team.eligible_bench))

    def pick_ability(self) -> None:
        abilities = self.team.active_elemental.available_abilities
        chosen_ability = self.roll(abilities)
        self.team.select_ability(chosen_ability)

    @staticmethod
    def roll(options: List) -> any:
        """
        Helper method that picks a random value out of a list of equal options.
        Typically returns Ability or CombatElemental.
        """
        pick = randint(0, len(options) - 1)
        return options[pick]
