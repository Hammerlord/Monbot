import unittest

from tests.character.character_builder import PlayerBuilder
from tests.character.user_builder import UserBuilder


class PlayerTests(unittest.TestCase):

    def setUp(self):
        self.user = UserBuilder().with_name("Dopple").build()
        self.player = PlayerBuilder().with_user(self.user).build()

    def tearDown(self):
        self.player = None

    def test_default_nickname(self):
        error = "Player nickname must be the user's name by default"
        self.assertEqual(self.player.nickname, "Dopple", error)

    def test_starter_creation(self):
        error = "A starter elemental must be created with the Player"
        team_size = self.player.team.size
        self.assertEqual(team_size, 1, error)

    def test_is_busy_combat(self):
        error = "Player is incorrectly able to enter combat while busy"
        # TODO

    def test_invalid_combat(self):
        error = "Player is incorrectly able to enter combat while all their Elementals are KOed"
        # TODO

    def test_is_busy_home(self):
        error = "Player is incorrectly able to view their Home while busy"
        # TODO

    def test_is_busy_elemental(self):
        error = "Player is incorrectly able to rank, fuse, etc... elementals while busy"
        # TODO

    def test_is_busy_travel(self):
        error = "Player is incorrectly able to travel while busy"
        # TODO

    def test_is_busy_shop(self):
        error = "Player is incorrectly able to shop while busy"
        # TODO
