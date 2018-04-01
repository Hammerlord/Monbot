import unittest

from src.character.character_builder import CharacterBuilder
from src.character.inventory import Inventory
from src.team.team import Team


class CharacterTests(unittest.TestCase):

    """
    Test the base Character class, which is the parent of NPC and character.
    """

    def setUp(self):
        self.character = CharacterBuilder().with_level(1).build()

    def tearDown(self):
        self.character = None

    def test_gain_exp(self):
        error = "Character couldn't acquire experience"
        self.character.add_exp(10)
        exp_gained = self.character.get_current_exp()
        self.assertEqual(exp_gained, 10, error)

    def test_level_exp_cap(self):
        error = "Instantiating a character didn't give it an exp requirement to level"
        exp_to_level = self.character.get_exp_to_level()
        self.assertGreater(exp_to_level, 0, error)

    def test_level_up(self):
        error = "Character couldn't level"
        exp_to_level = self.character.get_exp_to_level()
        before_level = self.character.get_level()
        self.character.add_exp(exp_to_level)
        after_level = self.character.get_level()
        self.assertGreater(after_level, before_level, error)

    def test_multi_level_up(self):
        error = "Character failed to level up multiple times with multiple levels' worth of experience"
        exp_gained = self.character.get_exp_to_level() * 5
        before_level = self.character.get_level()
        self.character.add_exp(exp_gained)
        after_level = self.character.get_level()
        self.assertGreater(after_level, before_level + 1, error)

    def test_max_level_exp_gain(self):
        error = "Character was incorrectly able to gain experience at max level"
        character = CharacterBuilder().with_level(60).build()
        character.add_exp(100)
        self.assertEqual(character.get_current_exp(), 0, error)

    def test_max_level_current_exp(self):
        error = "Character's current exp wasn't set to 0 at max level"
        character = CharacterBuilder().with_level(59).build()
        character.add_exp(100000)
        self.assertEqual(character.get_current_exp(), 0, error)

    def test_set_nickname(self):
        error = "Character nickname couldn't be set"
        name = "Amorphous Blob"
        self.character.set_nickname(name)
        self.assertEqual(self.character.get_nickname(), name, error)

    def test_nickname_max_length(self):
        error = "Character nickname can incorrectly be set to more than 15 characters"
        self.character.set_nickname("dsadadaifjasifjasfdsd")
        name_length = len(self.character.get_nickname())
        self.assertLessEqual(name_length, 15, error)

    def test_nickname_spaces(self):
        error = "Setting a nickname must strip the beginning and ending spaces"
        self.character.set_nickname("   hello")
        name_length = len(self.character.get_nickname())
        self.assertEqual(name_length, 5, error)
        self.assertEqual(self.character.get_nickname(), "hello", error)

    def test_has_inventory(self):
        error = "Character didn't set up an Inventory on instantiation"
        inventory = self.character.get_inventory()
        self.assertIsInstance(inventory, Inventory, error)

    def test_has_team(self):
        error = "Character didn't set up a Team on instantiation"
        team = self.character.get_team()
        self.assertIsInstance(team, Team, error)

