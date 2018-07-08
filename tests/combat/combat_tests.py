import unittest
from unittest.mock import Mock

from src.combat.combat import Combat
from src.combat.combat_actions import Switch, ElementalAction
from src.elemental.ability.abilities.claw import Claw
from src.elemental.ability.ability import Target
from src.elemental.combat_elemental import CombatElemental
from src.team.combat_team import CombatTeam
from tests.elemental.elemental_builder import ElementalBuilder
from tests.team.team_builder import TeamBuilder


class CombatTests(unittest.TestCase):

    def test_combat_set(self):
        error = "CombatTeam's combat property wasn't set on joining the battle"
        team = CombatTeam(TeamBuilder().build())
        combat = Combat()
        combat.join_battle(team)
        self.assertEqual(team.combat, combat, error)

    def test_rejoin_battle(self):
        error = "The same team can incorrectly join a battle multiple times"
        team_a = CombatTeam(TeamBuilder().build())
        combat = Combat()
        combat.join_battle(team_a)
        rejoined = combat.join_battle(team_a)
        self.assertFalse(rejoined, error)

    def test_get_enemy_target(self):
        error = "Ability that targets an enemy didn't get the correct target"
        team_a = self.get_combat_team()
        team_b = self.get_combat_team()
        combat = Combat()
        combat.join_battle(team_a)
        combat.join_battle(team_b)
        ability = Mock()
        ability.targeting = Target.ENEMY
        target = combat.get_target(ability, team_a.active_elemental)
        self.assertEqual(target, team_b.active_elemental, error)

    def test_get_self_target(self):
        error = "Ability that targets self didn't get the correct target"
        team_a = self.get_combat_team()
        team_b = self.get_combat_team()
        combat = Combat()
        combat.join_battle(team_a)
        combat.join_battle(team_b)
        ability = Mock()
        ability.targeting = Target.SELF
        target = combat.get_target(ability, team_a.active_elemental)
        self.assertEqual(target, team_a.active_elemental, error)

    def test_action_switch_priority(self):
        error = "Switch wasn't faster than a regular ability"
        team_a = self.get_combat_team()
        team_b = self.get_combat_team()
        combat = Combat()
        combat.join_battle(team_a)
        combat.join_battle(team_b)
        combat_elemental = CombatElemental(ElementalBuilder().build(), team_b)
        combat.request_action(Switch(team_a, combat_elemental, combat_elemental))
        combat.request_action(ElementalAction(combat_elemental, Claw(), combat_elemental))
        self.assertIsInstance(combat.previous_round_log[0], Switch, error)

    def test_action_speed_priority(self):
        error = "Faster elemental didn't attack first"
        team_a = self.get_combat_team()
        team_b = self.get_combat_team()
        combat = Combat()
        combat.join_battle(team_a)
        combat.join_battle(team_b)
        slower = CombatElemental(ElementalBuilder().with_level(1).build(), team_a)
        faster = CombatElemental(ElementalBuilder().with_level(10).with_nickname('loksy').build(), team_b)
        combat.request_action(ElementalAction(slower, Claw(), faster))
        faster_action = ElementalAction(faster, Claw(), slower)
        combat.request_action(faster_action)
        expected = combat.previous_round_log[0].actor.nickname
        self.assertEqual(expected, faster.nickname, error)

    @staticmethod
    def get_combat_team():
        """
        :return: A CombatTeam with an elemental in it.
        """
        team = TeamBuilder().build()
        team.add_elemental(ElementalBuilder().build())
        return CombatTeam(team)
