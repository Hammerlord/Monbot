import unittest
from unittest.mock import Mock

from src.combat.actions.combat_actions import Switch
from src.combat.actions.elemental_action import ElementalAction
from src.combat.combat import Combat
from src.elemental.ability.abilities.claw import Claw
from src.elemental.ability.abilities.defend import Defend
from src.elemental.ability.abilities.shining_laser import ShiningLaser
from src.elemental.ability.queueable import Castable
from src.elemental.combat_elemental import CombatElemental
from src.team.combat_team import CombatTeam
from tests.character.character_builder import PlayerBuilder
from tests.elemental.elemental_builder import ElementalBuilder, CombatElementalBuilder
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

    def test_action_switch_priority(self):
        error = "Switch wasn't faster than a regular ability"
        team_a = self.get_combat_team()
        team_b = self.get_combat_team()
        combat = Combat()
        combat.join_battle(team_a)
        combat.join_battle(team_b)
        combat_elemental = CombatElemental(ElementalBuilder().build(), team_b)
        combat.request_action(ElementalAction(combat_elemental, Claw(), combat_elemental))
        combat.request_action(Switch(team_a, combat_elemental, combat_elemental))
        self.assertIsInstance(combat.previous_round_actions[0], Switch, error)

    def test_defend_priority(self):
        error = "Defend wasn't faster than other abilities"
        team_a = self.get_combat_team()
        team_b = self.get_combat_team()
        combat = Combat()
        combat.join_battle(team_a)
        combat.join_battle(team_b)
        faster = CombatElemental(ElementalBuilder().with_speed(10).build(), team_b)
        team_b.change_active_elemental(faster)
        slower = CombatElemental(ElementalBuilder().with_speed(1).build(), team_a)
        team_a.change_active_elemental(slower)
        combat.request_action(ElementalAction(faster, Claw(), slower))
        combat.request_action(ElementalAction(slower, Defend(), slower))
        self.assertIsInstance(combat.previous_round_actions[0].ability, Defend, error)

    def test_action_speed_priority(self):
        error = "Faster elemental didn't attack first"
        team_a = self.get_combat_team()
        team_b = self.get_combat_team()
        combat = Combat()
        combat.join_battle(team_a)
        combat.join_battle(team_b)
        slower = CombatElemental(ElementalBuilder().with_level(1).build(), team_a)
        team_a.change_active_elemental(slower)
        faster = CombatElemental(ElementalBuilder().with_level(10).with_nickname('loksy').build(), team_b)
        team_b.change_active_elemental(faster)
        combat.request_action(ElementalAction(slower, Claw(), faster))
        faster_action = ElementalAction(faster, Claw(), slower)
        combat.request_action(faster_action)
        expected = combat.previous_round_actions[0].actor.nickname
        self.assertEqual(expected, faster.nickname, error)

    def test_elemental_exp_gain(self):
        error = "Knocking out an elemental didn't grant exp to player's elementals"
        player = PlayerBuilder().build()
        player_team = TeamBuilder().with_owner(player).build()
        elemental = ElementalBuilder().with_level(5).build()
        player_team.add_elemental(elemental)
        player_team = CombatTeam(player_team)
        other_team = self.get_combat_team()
        combat = Combat()
        combat.join_battle(player_team)
        combat.join_battle(other_team)
        other_team.elementals[0].receive_damage(10000, player_team.elementals[0])
        exp_before = elemental.current_exp
        player_team.make_move(Claw())
        other_team.make_move(Claw())
        exp_after = elemental.current_exp
        self.assertGreater(exp_after, exp_before, error)

    def test_player_exp_gain(self):
        error = "Knocking out an elemental didn't grant exp to player"
        player = PlayerBuilder().build()
        player_team = TeamBuilder().with_owner(player).build()
        player_team.add_elemental(ElementalBuilder().build())
        player_team = CombatTeam(player_team)
        other_team = self.get_combat_team()
        combat = Combat()
        combat.join_battle(player_team)
        combat.join_battle(other_team)
        other_team.elementals[0].receive_damage(10000, player_team.elementals[0])
        exp_before = player.current_exp
        player_team.make_move(Claw())
        other_team.make_move(Claw())
        exp_after = player.current_exp
        self.assertGreater(exp_after, exp_before, error)

    def test_cast_time_wait(self):
        error = "A one turn cast spell resolved immediately"
        team_a = self.get_combat_team()
        team_b = self.get_combat_team()
        combat = Combat()
        combat.join_battle(team_a)
        combat.join_battle(team_b)
        elemental_b = team_b.elementals[0]
        health_before = elemental_b.current_hp
        team_a.handle_cast_time(Castable(ShiningLaser()))
        team_b.make_move(Claw())
        self.assertEqual(elemental_b.current_hp, health_before, error)

    def test_cast_recap(self):
        error = "Recap message was incorrect for a cast time spell"
        team_a = self.get_combat_team()
        team_b = self.get_combat_team()
        combat = Combat()
        combat.join_battle(team_a)
        combat.join_battle(team_b)
        elemental_a = team_a.elementals[0]
        team_a.handle_cast_time(Castable(ShiningLaser()))
        team_b.make_move(Claw())
        self.assertEqual(elemental_a.last_action.recap, 'Thefaketofu is shining mightily!!', error)

    def test_cast_time_resolution(self):
        error = "Casted spell didn't resolve when ready"
        team_a = self.get_combat_team()
        team_b = self.get_combat_team()
        combat = Combat()
        combat.join_battle(team_a)
        combat.join_battle(team_b)
        elemental_b = team_b.elementals[0]
        health_before = elemental_b.current_hp
        team_b.make_move(Defend())
        team_a.handle_cast_time(Castable(ShiningLaser()))
        team_b.make_move(Claw())
        self.assertLess(elemental_b.current_hp, health_before, error)

    def test_elemental_action(self):
        error = "ElementalAction could incorrectly trigger when the elemental is KOed."
        team = TeamBuilder().build()
        elemental = ElementalBuilder().build()
        team.add_elemental(elemental)
        team = CombatTeam(team)
        elemental.receive_damage(10000)
        action = ElementalAction(
            actor=team.elementals[0],
            ability=Claw(),
            target=Mock()
        )
        self.assertFalse(action.can_execute, error)

    def test_active_elemental_action(self):
        error = "ElementalAction could incorrectly trigger when the elemental forcibly switched."
        team = TeamBuilder().build()
        elemental = ElementalBuilder().build()
        team.add_elemental(elemental)
        team = CombatTeam(team)
        old_active = team.elementals[0]
        team.change_active_elemental(old_active)
        team.change_active_elemental(CombatElementalBuilder().build())
        action = ElementalAction(
            actor=old_active,
            ability=Claw(),
            target=Mock()
        )
        self.assertFalse(action.can_execute, error)

    @staticmethod
    def get_combat_team():
        """
        :return: A CombatTeam with an elemental in it.
        """
        team = TeamBuilder().build()
        team.add_elemental(ElementalBuilder().build())
        return CombatTeam(team)
