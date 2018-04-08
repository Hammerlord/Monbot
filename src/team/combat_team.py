from typing import List

from src.elemental.combat_elemental import CombatElemental
from src.team.team import Team


class CombatTeam:

    """
    Wrapper class for a Team in battle. Generates CombatElemental instances of the Team's Elementals.
    TODO entering combat should fail if all Elementals have been knocked out.
    """

    def __init__(self, team: Team):
        self.team = [CombatElemental(elemental) for elemental in team.elementals]
        self.owner = team.owner
        self._active = self.set_next_active()
        self.status_effects = []  # Team-wide status effects, eg. weather.
        self.actions = []  # A stack of CombatActions taken by this team.

    def set_next_active(self) -> CombatElemental:
        """
        The next Elemental eligible to be active (HP > 0), meaning it is sent to the battlefield.
        """
        return next((elemental for elemental in self.team if not elemental.is_knocked_out), None)

    @property
    def is_npc(self) -> bool:
        return self.owner.is_npc

    @property
    def is_all_knocked_out(self) -> bool:
        """
        :return: If all Elementals on the Team have been knocked out (0 HP).
        Game over if true.
        """
        return all(elemental.is_knocked_out for elemental in self.team)

    def switch(self, slot: int) -> None:
        """
        Switch the active Elemental with an Elemental on CombatTeam.bench.
        """
        if not self.can_switch(slot):
            return
        self._active = self.bench[slot]

    @property
    def active(self) -> CombatElemental:
        return self._active

    @property
    def bench(self) -> List[CombatElemental]:
        """
        Returns the team CombatElementals minus the active one.
        """
        return [elemental for elemental in self.team if elemental != self._active]

    def can_switch(self, slot: int) -> bool:
        """
        Check if the impending position is a valid slot.
        """
        max_slots = len(self.team) - 1  # The number of Elementals on the team minus the active one.
        return 0 <= slot < max_slots
