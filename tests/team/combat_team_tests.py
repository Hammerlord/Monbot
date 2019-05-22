import unittest
from unittest.mock import Mock

from src.combat.combat import Combat
from src.elemental.ability.ability import Target
from src.elemental.combat_elemental import CombatElemental
from src.team.combat_team import CombatTeam
from src.team.team import Team
from tests.character.character_builder import NPCBuilder, PlayerBuilder
from tests.elemental.elemental_builder import ElementalBuilder
from tests.team.team_builder import TeamBuilder


class CombatTeamTests(unittest.TestCase):

    def test_setup_active(self):
        error = "CombatTeam didn't assign an active CombatElemental on combat start"
        team = CombatTeam([ElementalBuilder().build()])
        Combat([team], [], Mock())
        self.assertIsInstance(
            team.active_elemental,
            CombatElemental, error)

    def test_skip_ko_active(self):
        error = "CombatTeam incorrectly set a 0 HP Elemental as the active Elemental"
        team = CombatTeam([
            ElementalBuilder().with_current_hp(0).build(),
            ElementalBuilder().build()
        ])
        Combat([team], [], Mock())
        self.assertGreater(team.active_elemental.current_hp, 0, error)

    def test_is_npc(self):
        error = "CombatTeam didn't flag itself as NPC when its owner was an NPC"
        npc = NPCBuilder().build()
        combat_team = CombatTeam([ElementalBuilder().build()], npc)
        self.assertIs(combat_team.is_npc, True, error)

    def test_bench(self):
        error = "CombatTeam incorrectly included the active CombatElemental in bench"
        team = CombatTeam([
            ElementalBuilder().build(),
            ElementalBuilder().build()
        ])
        Combat([team], [], Mock())
        self.assertEqual(len(team.bench), 1, error)
        self.assertEqual(team.bench[0].id, team.elementals[0].id, error)

    def test_eligible_bench(self):
        error = "CombatTeam incorrectly included knocked out CombatElementals in the eligible bench"
        team = CombatTeam([
            ElementalBuilder().with_current_hp(0).build(),
            ElementalBuilder().build()
        ])
        Combat([team], [], Mock())
        self.assertEqual(len(team.eligible_bench), 0, error)

    def test_switch_ko(self):
        error = "CombatTeam incorrectly allowed a knocked out CombatElemental to be switched in"
        team = CombatTeam([
            ElementalBuilder().with_current_hp(0).build(),
            ElementalBuilder().build()
        ])
        Combat([team], [], Mock())
        is_switched = team.attempt_switch(team.elementals[0])
        self.assertFalse(is_switched, error)

    def test_all_knocked_out(self):
        error = "CombatTeam.is_all_knocked_out didn't resolve correctly"
        team = CombatTeam([
            ElementalBuilder().with_current_hp(0).build(),
        ])
        self.assertIs(team.is_all_knocked_out, True, error)

    def test_mana_per_turn(self):
        error = "CombatTeam eligible Elementals on the bench didn't gain mana on turn start"
        team = CombatTeam([
            ElementalBuilder().build(),
            ElementalBuilder().build()
        ])
        Combat([team], [], Mock())
        bench = team.eligible_bench
        starting_mana = bench[0].current_mana
        team.turn_start()
        resultant_mana = bench[0].current_mana
        self.assertGreater(resultant_mana, starting_mana, error)

    def test_team_defensive_copy(self):
        error = "Changing the member of a Team incorrectly affected the CombatTeam"
        # Not that it should be possible to change your elementals when you're in combat.
        team = TeamBuilder().build()
        combat_team = CombatTeam.from_team(team)
        team.remove_elemental(0)
        self.assertEqual(len(combat_team.elementals), 1, error)

    def test_get_enemy_target(self):
        error = "Ability that targets an enemy didn't get the correct target"
        team_a = CombatTeam([ElementalBuilder().build()], PlayerBuilder().build())
        team_b = CombatTeam([ElementalBuilder().build()], PlayerBuilder().build())
        combat = Combat([team_a], [team_b], Mock())
        ability = Mock()
        ability.targeting = Target.ENEMY
        target = combat.get_target(ability, team_a.active_elemental)
        self.assertEqual(target, team_b.active_elemental, error)

    def test_get_self_target(self):
        error = "Ability that targets self didn't get the correct target"
        team_a = CombatTeam([ElementalBuilder().build()], PlayerBuilder().build())
        team_b = CombatTeam([ElementalBuilder().build()], PlayerBuilder().build())
        combat = Combat([team_a], [team_b], Mock())
        ability = Mock()
        ability.targeting = Target.SELF
        target = combat.get_target(ability, team_a.active_elemental)
        self.assertEqual(target, team_a.active_elemental, error)
