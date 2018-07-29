from src.character.npc_initializer import NPCInitializer
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
        self.npc_two.generate_team(self.npc_one)

    def fight(self):
        combat = Combat()
        team_one = CombatTeam(self.npc_one.team)
        team_two = CombatTeam(self.npc_two.team)
        combat.join_battle(team_one)
        combat.join_battle(team_two)


SimulatedBattle().fight()
