import unittest


class NPCTests(unittest.TestCase):

    """
    NPCs automatically generate a Team that:
    1) suits the opposing Player's level and team size
    2) fits their profession (eg. Researcher, Enthusiast, Adventurer)
    """

    def test_is_npc(self):
        error = "NPC wasn't flagged as an npc"
        npc = NPCBuilder().build()
        self.assertTrue(npc.is_npc)

    def test_team(self):
        error = "NPC team didn't start with any elementals"
        npc = NPCBuilder().build()
        npc_team_size = npc.get_team().get_size()
        self.assertGreater(npc_team_size, 0, error)

    def test_team_size(self):
        error = "NPC team size is potentially larger than the opponent's"
        for i in range(100):
            player = PlayerBuilder().build()
            npc = NPCBuilder().with_opponent(player).build()
            player_team_size = player.get_team().get_size()
            npc_team_size = npc.get_team().get_size()
            self.assertLessEqual(npc_team_size, player_team_size, error)

    def test_max_level(self):
        error = "NPC level is potentially too much higher than the opponent's"
        for i in range(100):
            player = PlayerBuilder().with_level(10).build()
            npc = NPCBuilder().with_opponent(player).build()
            accepted_max_level = player.level + 1
            self.assertLessEqual(npc.level, accepted_max_level, error)

    def test_min_level(self):
        error = "NPC level is potentially too much lower than the opponent's"
        for i in range(100):
            player = PlayerBuilder().with_level(10).build()
            npc = NPCBuilder().with_opponent(player).build()
            accepted_min_level = player.level - 2
            self.assertGreaterEqual(npc.level, accepted_min_level, error)

    def test_valid_level(self):
        error = "NPC level is potentially less than 1"
        for i in range(100):
            player = PlayerBuilder().with_level(1).build()
            npc = NPCBuilder().with_opponent(player).build()
            self.assertGreaterEqual(npc.level, 1, error)

    def test_team_level(self):
        error = "NPC's elemental levels are potentially higher than his own level"
        for i in range(100):
            npc = NPCBuilder().build()
            team = npc.get_team()
            for elemental in team.get_elementals():
                self.assertLessEqual(elemental.level, npc.level, error)

    def test_profession_elementals(self):
        error = "A Researcher's elementals don't match his profession"
        researcher = NPCBuilder().researcher()
        team = researcher.get_team()
        pool = researcher.potential_elementals()
        for elemental in team.get_elementals():
            self.assertIn(elemental, pool, error)

    def test_default_nickname(self):
        error = "NPC nickname must default to a string"
        npc = NPCBuilder().random()
        self.assertIsInstance(npc.nickname, str, error)

    def test_researcher_name(self):
        error = "A Researcher is not called a Researcher as his nickname"
        researcher = NPCBuilder().researcher()
        self.assertEquals(researcher.nickname, "Researcher", error)
