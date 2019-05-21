from unittest.mock import Mock

from src.character.npc.npc_initializer import NPCInitializer
from src.combat.combat import Combat
from src.team.combat_team import CombatTeam


class SimulatedBattle:
    """
    An auto battle between two NPCs.
    """
    def __init__(self):
        self.npc_one = NPCInitializer.collector()
        self.npc_one.generate_random_team(min_level=10,
                                          max_level=10,
                                          min_team_size=4)
        self.npc_two = NPCInitializer().collector()
        self.npc_two.generate_equal_team(self.npc_one)

    def fight(self):
        Combat([CombatTeam(self.npc_one.team)],
               [CombatTeam(self.npc_two.team)],
               Mock())


SimulatedBattle().fight()
