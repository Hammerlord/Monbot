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
        self.assertEqual(self.team.get_size(), 4, error)
        self.assertEqual(self.team.is_space_available(), False, error)

    def test_reorder_elementals(self):
        error = "Failed to reorder Elementals in a Team"
        elemental_a = ElementalBuilder().with_id(1).build()
        elemental_b = ElementalBuilder().with_id(2).build()
        team = TeamBuilder.build()
        team.add_elemental(elemental_a)  # Position 0
        team.add_elemental(elemental_b)  # Position 1
        team.reorder(0, 1)
        self.assertEqual(elemental_a.id, team.get_elemental(1).id, error)
        self.assertEqual(elemental_b.id, team.get_elemental(0).id, error)
