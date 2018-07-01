import unittest

from tests.character.character_builder import NPCBuilder, PlayerBuilder
from tests.elemental.elemental_builder import ElementalBuilder


class NPCTests(unittest.TestCase):
    """
    NPCs automatically generate a Team that:
    1) suits the opposing Player's level and team size (slightly randomized)
    2) fits their profession (eg. Researcher, Enthusiast, Adventurer)
    """

    def get_player(self):
        """
        :return: A Player object with 2 Elementals on their Team.
        """
        player = PlayerBuilder().with_level(10).build()
        player.add_elemental(ElementalBuilder().build())
        player.add_elemental(ElementalBuilder().build())
        return player

    def test_is_npc(self):
        error = "NPC wasn't flagged as an npc"
        npc = NPCBuilder().build()
        self.assertTrue(npc.is_npc, error)

    def test_team(self):
        error = "NPC team didn't start with any Elementals"
        npc = NPCBuilder().build()
        npc_team_size = npc.team.size
        self.assertGreater(npc_team_size, 0, error)

    def test_team_size(self):
        error = "NPC team size is potentially larger than the opponent's"
        is_correct_size = True
        player = self.get_player()
        for i in range(100):
            npc = NPCBuilder().with_opponent(player).build()
            if npc.team.size > player.team.size:
                is_correct_size = False
                break
        self.assertTrue(is_correct_size, error)

    def test_max_level(self):
        error = "NPC level is potentially too much higher than the opponent's"
        is_correct_level = True
        player = self.get_player()
        for i in range(100):
            npc = NPCBuilder().with_opponent(player).build()
            accepted_max_level = player.level + 1
            if npc.level > accepted_max_level:
                is_correct_level = False
                break
        self.assertTrue(is_correct_level, error)

    def test_min_level(self):
        error = "NPC level is potentially too much lower than the opponent's"
        is_correct_level = True
        player = self.get_player()
        for i in range(100):
            npc = NPCBuilder().with_opponent(player).build()
            accepted_min_level = player.level - 2
            if npc.level < accepted_min_level:
                is_correct_level = False
                break
        self.assertTrue(is_correct_level, error)

    def test_valid_level(self):
        error = "NPC level is potentially less than 1"
        is_correct_level = True
        player = PlayerBuilder().with_level(1).build()
        for i in range(100):
            npc = NPCBuilder().with_opponent(player).build()
            if npc.level < 1:
                is_correct_level = False
                break
        self.assertTrue(is_correct_level, error)

    def test_team_level(self):
        error = "NPC's elemental levels are potentially higher than his own level"
        is_correct_level = True
        for i in range(100):
            npc = NPCBuilder().build()
            team = npc.team
            for elemental in team.elementals:
                if elemental.level > npc.level:
                    is_correct_level = False
                    break
        self.assertTrue(is_correct_level, error)

    def test_profession_elementals(self):
        error = "An NPC's elementals don't match potential species"
        npc = NPCBuilder().build()
        team = npc.team
        pool = npc._potential_species
        is_correct = True
        for i in range(100):
            for elemental in team.elementals:
                if elemental.species not in pool:
                    is_correct = False
                    break
        self.assertTrue(is_correct, error)

    def test_default_nickname(self):
        error = "NPC nickname doesn't get set"
        npc = NPCBuilder().build()
        self.assertIsInstance(npc.nickname, str, error)
