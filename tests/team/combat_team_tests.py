import unittest
from unittest.mock import Mock

from src.combat.combat import Combat
from src.elemental.combat_elemental import CombatElemental
from src.team.combat_team import CombatTeam
from src.team.team import Team
from tests.character.character_builder import NPCBuilder, PlayerBuilder
from tests.elemental.elemental_builder import ElementalBuilder
from tests.team.team_builder import TeamBuilder


class CombatTeamTests(unittest.TestCase):

    @staticmethod
    def get_combat_team(team) -> CombatTeam:
        """
        :return: A test CombatTeam with two Elementals.
        """
        combat_team = CombatTeam(team)
        combat_team.set_combat(Combat())
        combat_team.on_combat_start()  # Triggers the initial switch in.
        return combat_team

    @staticmethod
    def get_team() -> Team:
        team = TeamBuilder().build()
        smurggle = ElementalBuilder().build()
        loksy = ElementalBuilder().build()
        team.add_elemental(smurggle)
        team.add_elemental(loksy)
        return team

    def test_setup_active(self):
        error = "CombatTeam didn't assign an active CombatElemental on combat start"
        self.assertIsInstance(
            self.get_combat_team(self.get_team()).active_elemental,
            CombatElemental, error)

    def test_skip_ko_active(self):
        error = "CombatTeam incorrectly set a 0 HP Elemental as the active Elemental"
        team = TeamBuilder().build()
        smurggle = ElementalBuilder().with_current_hp(0).build()
        loksy = ElementalBuilder().build()
        team.add_elemental(smurggle)
        team.add_elemental(loksy)
        combat_team = self.get_combat_team(team)
        self.assertEqual(combat_team.active_elemental.id, loksy.id, error)

    def test_is_npc(self):
        error = "CombatTeam didn't flag itself as NPC when its owner was an NPC"
        npc = NPCBuilder().build()
        team = TeamBuilder().with_owner(npc).build()
        combat_team = CombatTeam(team)
        self.assertIs(combat_team.is_npc, True, error)

    def test_bench(self):
        error = "CombatTeam incorrectly included the active CombatElemental in bench"
        team = TeamBuilder().build()
        smurggle = ElementalBuilder().build()
        loksy = ElementalBuilder().build()
        team.add_elemental(smurggle)
        team.add_elemental(loksy)
        combat_team = self.get_combat_team(team)
        bench = combat_team.bench
        self.assertEqual(len(bench), 1, error)
        self.assertEqual(bench[0].id, loksy.id, error)

    def test_eligible_bench(self):
        error = "CombatTeam incorrectly included knocked out CombatElementals in the eligible bench"
        team = TeamBuilder().build()
        smurggle = ElementalBuilder().with_current_hp(0).build()
        loksy = ElementalBuilder().build()
        team.add_elemental(smurggle)
        team.add_elemental(loksy)  # Loksy should be considered active
        combat_team = self.get_combat_team(team)
        bench = combat_team.eligible_bench
        self.assertEqual(len(bench), 0, error)

    def test_switch_ko(self):
        error = "CombatTeam incorrectly allowed a knocked out CombatElemental to be switched in"
        team = TeamBuilder().build()
        smurggle = ElementalBuilder().with_current_hp(0).build()
        loksy = ElementalBuilder().build()
        team.add_elemental(smurggle)
        team.add_elemental(loksy)
        combat_team = self.get_combat_team(team)
        is_switched = combat_team.attempt_switch(0)
        self.assertFalse(is_switched, error)

    def test_switch_log(self):
        error = "Switching didn't create a log as the most recent action"
        owner = PlayerBuilder().with_nickname('Dopple').build()
        team = TeamBuilder().with_owner(owner).build()
        smurggle = ElementalBuilder().with_nickname('smurggle').build()
        loksy = ElementalBuilder().with_nickname('loksy').build()
        team.add_elemental(smurggle)
        team.add_elemental(loksy)
        combat_team = self.get_combat_team(team)
        combat_team.attempt_switch(0)
        action = combat_team.last_action
        self.assertEqual(action.recap, 'Dopple recalled smurggle and sent out loksy!', error)

    def test_all_knocked_out(self):
        error = "CombatTeam.is_all_knocked_out didn't resolve correctly"
        team = TeamBuilder().build()
        smurggle = ElementalBuilder().with_current_hp(0).build()
        team.add_elemental(smurggle)
        combat_team = CombatTeam(team)
        self.assertIs(combat_team.is_all_knocked_out, True, error)

    def test_mana_per_turn(self):
        error = "CombatTeam eligible Elementals on the bench didn't gain mana on turn start"
        combat_team = self.get_combat_team(self.get_team())
        bench = combat_team.eligible_bench
        starting_mana = bench[0].current_mana
        combat_team.on_turn_start()
        resultant_mana = bench[0].current_mana
        self.assertGreater(resultant_mana, starting_mana, error)

    def test_team_defensive_copy(self):
        error = "Changing the member of a Team incorrectly affected the CombatTeam"
        # Not that it should be possible to change your elementals when you're in combat.
        team = TeamBuilder().build()
        smurggle = ElementalBuilder().build()
        team.add_elemental(smurggle)
        combat_team = CombatTeam(team)
        team.remove_elemental(0)
        self.assertEqual(len(combat_team.elementals), 1, error)
