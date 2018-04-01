import unittest


class TeamTests(unittest.TestCase):
    def setUp(self):
        self.team = TeamBuilder().build()

    def tearDown(self):
        self.team.dispose()
        self.team = None

    def test_max_num_elementals(self):
        error = "A Team can incorrectly have more than 4 Elementals"
        for i in range(5):
            elemental = ElementalBuilder().build()
            self.team.add_elemental(elemental)
        self.assertEquals(self.team.get_size(), 4, error)
        self.assertEquals(self.team.is_space_available(), False, error)

    def test_reorder_elementals(self):
        error = "Failed to reorder Elementals in a Team"
        elemental_a = ElementalBuilder().with_id(1).build()
        elemental_b = ElementalBuilder().with_id(2).build()
        team = TeamBuilder.build()
        team.add_elemental(elemental_a)  # Position 0
        team.add_elemental(elemental_b)  # Position 1
        team.reorder(0, 1)
        self.assertEquals(elemental_a.id, team.get_elemental(1).id, error)
        self.assertEquals(elemental_b.id, team.get_elemental(0).id, error)


class CombatTeamTests(unittest.TestCase):

    def setUp(self):
        team = TeamBuilder().build()
        smurggle = ElementalBuilder().with_id(1).build()
        loksy = ElementalBuilder().with_id(2).build()
        team.add_elemental(smurggle)
        team.add_elemental(loksy)
        self.combat_team = CombatTeamBuilder().with_team(team).build()

    def tearDown(self):
        self.combat_team.dispose()
        self.combat_team = None

    def test_setup_active(self):
        error = "CombatTeam didn't assign an active CombatElemental when created"
        self.assertIsInstance(self.combat_team.get_active(), CombatElemental, error)

    def test_skip_ko_active(self):
        error = "CombatTeam incorrectly set a 0 HP Elemental as the active Elemental"
        team = TeamBuilder().build()
        smurggle = ElementalBuilder().with_id(1).with_hp(0).build()
        loksy = ElementalBuilder().with_id(2).build()
        team.add_elemental(smurggle)
        team.add_elemental(loksy)
        combat_team = CombatTeamBuilder().with_team(team).build()
        self.assertEquals(combat_team.get_active().id, loksy.id, error)

    def test_is_npc(self):
        error = "CombatTeam didn't flag itself as NPC when its owner was an NPC"
        # TODO

    def test_bench(self):
        error = "CombatTeam incorrectly included the active CombatElemental in get_bench()"
        bench = self.combat_team.get_bench()
        self.assertEquals(len(bench), 1, error)
        self.assertEquals(bench[0].id, 2, error)  # Loksy's id, see setUp

