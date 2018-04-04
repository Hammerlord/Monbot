import unittest

from src.character.inventory import Inventory
from src.team.team import Team
from tests.character.character_builder import CharacterBuilder


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
        self.character.add_exp(4)
        exp_gained = self.character.current_exp
        self.assertEqual(exp_gained, 4, error)

    def test_level_exp_cap(self):
        error = "Instantiating a character didn't give it an exp requirement to level"
        exp_to_level = self.character.exp_to_level
        self.assertGreater(exp_to_level, 0, error)

    def test_level_up(self):
        error = "Character couldn't level"
        exp_to_level = self.character.exp_to_level
        before_level = self.character.level
        self.character.add_exp(exp_to_level)
        after_level = self.character.level
        self.assertGreater(after_level, before_level, error)

    def test_multi_level_up(self):
        error = "Character failed to level up multiple times with multiple levels' worth of experience"
        exp_gained = self.character.exp_to_level * 5
        before_level = self.character.level
        self.character.add_exp(exp_gained)
        after_level = self.character.level
        self.assertGreater(after_level, before_level + 1, error)

    def test_max_level_exp_gain(self):
        error = "Character was incorrectly able to gain experience at max level"
        character = CharacterBuilder().with_level(60).build()
        character.add_exp(100)
        self.assertEqual(character.current_exp, 0, error)

    def test_max_level_current_exp(self):
        error = "Character's current exp wasn't set to 0 at max level"
        character = CharacterBuilder().with_level(59).build()
        exp = character.exp_to_level + 5
        character.add_exp(exp)
        self.assertEqual(character.current_exp, 0, error)

    def test_set_nickname(self):
        error = "Character nickname couldn't be set"
        name = "Amorphous Blob"
        self.character.nickname = name
        self.assertEqual(self.character.nickname, name, error)

    def test_nickname_max_length(self):
        error = "Character nickname can incorrectly be set to more than 15 characters"
        self.character.nickname = "dsadadaifjasifjasfdsd"
        name_length = len(self.character.nickname)
        self.assertLessEqual(name_length, 15, error)

    def test_nickname_spaces(self):
        error = "Setting a nickname must strip the beginning and ending spaces"
        self.character.nickname = "   hello"
        name_length = len(self.character.nickname)
        self.assertEqual(name_length, 5, error)
        self.assertEqual(self.character.nickname, "hello", error)

    def test_has_inventory(self):
        error = "Character didn't set up an Inventory on instantiation"
        inventory = self.character.inventory
        self.assertIsInstance(inventory, Inventory, error)

    def test_has_team(self):
        error = "Character didn't set up a Team on instantiation"
        team = self.character.team
        self.assertIsInstance(team, Team, error)

