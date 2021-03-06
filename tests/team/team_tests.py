import unittest

from tests.elemental.elemental_builder import ElementalBuilder
from tests.team.team_builder import TeamBuilder


class TeamTests(unittest.TestCase):
    def setUp(self):
        self.team = TeamBuilder().build()  # Team with 1 Elemental

    def tearDown(self):
        self.team = None

    def test_max_num_elementals(self):
        error = "A Team can incorrectly have more than 4 Elementals"
        for i in range(5):
            elemental = ElementalBuilder().build()
            self.team.add_elemental(elemental)
        self.assertEqual(self.team.size, 4, error)
        self.assertEqual(self.team.is_space_available, False, error)

    def test_reorder_elementals(self):
        error = "Failed to reorder Elementals in a Team"
        monze = ElementalBuilder().build()
        lofy = ElementalBuilder().build()
        self.team.add_elemental(monze)  # Position 0
        self.team.add_elemental(lofy)  # Position 1
        self.team.reorder(0, 1)
        self.assertEqual(monze.id, self.team.get_elemental(1).id, error)
        self.assertEqual(lofy.id, self.team.get_elemental(0).id, error)

    def test_swap_elemental(self):
        error = "Failed to swap Elementals in a valid Team slot"
        monze = ElementalBuilder().build()
        lofy = ElementalBuilder().build()
        self.team.add_elemental(monze)  # Position 0
        self.team.swap(slot=0, elemental=lofy)
        self.assertEqual(lofy.id, self.team.get_elemental(0).id, error)

    def test_out_of_bounds_swap(self):
        error = "Incorrectly swapped in an Elemental to an out of bounds Team slot"
        monze = ElementalBuilder().build()
        self.team.swap(slot=-1, elemental=monze)
        self.team.swap(slot=5, elemental=monze)
        self.assertEqual(self.team.size, 1, error)

    def test_reorder_empty(self):
        error = "Incorrectly reordered an Elemental into an empty slot"
        monze = ElementalBuilder().build()
        self.team.add_elemental(monze)
        self.team.reorder(0, 3)
        self.assertEqual(monze.id, self.team.get_elemental(0).id, error)

    def test_remove_elemental(self):
        error = "Failed to remove an Elemental from the Team"
        monze = ElementalBuilder().build()
        lofy = ElementalBuilder().build()
        self.team.add_elemental(monze)  # Position 0
        self.team.add_elemental(lofy)  # Position 1
        self.team.remove_elemental(0)  # Remove monze
        self.assertEqual(lofy.id, self.team.get_elemental(0).id, error)
