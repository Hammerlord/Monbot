import unittest

from src.elemental.combat_elemental import CombatElemental
from src.team.combat_team import CombatTeam
from tests.elemental.elemental_builder import ElementalBuilder
from tests.team.team_builder import TeamBuilder


class CombatTeamTests(unittest.TestCase):

    def setUp(self):
        team = TeamBuilder().build()
        smurggle = ElementalBuilder().with_id(1).build()
        loksy = ElementalBuilder().with_id(2).build()
        team.add_elemental(smurggle)
        team.add_elemental(loksy)
        self.combat_team = CombatTeam(team)

    def tearDown(self):
        self.combat_team = None

    def test_setup_active(self):
        error = "CombatTeam didn't assign an active CombatElemental when created"
        self.assertIsInstance(self.combat_team.active, CombatElemental, error)

    def test_skip_ko_active(self):
        error = "CombatTeam incorrectly set a 0 HP Elemental as the active Elemental"
        team = TeamBuilder().build()
        smurggle = ElementalBuilder().with_id(1).with_current_hp(0).build()
        loksy = ElementalBuilder().with_id(2).build()
        team.add_elemental(smurggle)
        team.add_elemental(loksy)
        combat_team = CombatTeam(team)
        self.assertEqual(combat_team.active.id, loksy.id, error)

    def test_is_npc(self):
        error = "CombatTeam didn't flag itself as NPC when its owner was an NPC"
        # TODO

    def test_bench(self):
        error = "CombatTeam incorrectly included the active CombatElemental in bench"
        bench = self.combat_team.bench
        self.assertEqual(len(bench), 1, error)
        self.assertEqual(bench[0].id, 2, error)  # Loksy's id, see setUp

    def test_switch(self):
        error = "CombatTeam incorrectly allowed a knocked out CombatElemental to be switched in"
        team = TeamBuilder().build()
        smurggle = ElementalBuilder().with_id(1).with_current_hp(0).build()
        loksy = ElementalBuilder().with_id(2).build()
        team.add_elemental(smurggle)
        team.add_elemental(loksy)
        combat_team = CombatTeam(team)
        combat_team.switch(0)  # smurggle's position
        self.assertEqual(combat_team.active.id, loksy.id, error)