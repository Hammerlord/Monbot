import unittest
from unittest.mock import Mock

from src.combat.combat import Combat
from src.elemental.ability.ability import Target
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

    @staticmethod
    def get_combat_team():
        """
        :return: A CombatTeam with an elemental in it.
        """
        team = TeamBuilder().build()
        team.add_elemental(ElementalBuilder().build())
        return CombatTeam(team)