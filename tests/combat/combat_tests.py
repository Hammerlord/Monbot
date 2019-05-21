import unittest
from unittest.mock import Mock

from src.combat.actions.combat_actions import Switch
from src.combat.actions.elemental_action import ElementalAction
from src.combat.combat import Combat
from src.elemental.ability.abilities.claw import Claw
from src.elemental.ability.abilities.defend import Defend
from src.elemental.ability.abilities.rampage import Rampage
from src.elemental.ability.abilities.shining_laser import ShiningLaser
from src.elemental.ability.queueable import Castable
from src.elemental.combat_elemental import CombatElemental
from src.team.combat_team import CombatTeam
from tests.character.character_builder import PlayerBuilder
from tests.elemental.elemental_builder import ElementalBuilder, CombatElementalBuilder
from tests.team.team_builder import TeamBuilder


def get_mocked_combat(team_a=None, team_b=None) -> Combat:
    return Combat(
        [team_a or CombatTeam(TeamBuilder().build())],
        [team_b or CombatTeam(TeamBuilder().build())],
        data_manager=Mock()
    )

class CombatTests(unittest.TestCase):

    def test_combat_set(self):
        error = "CombatTeam's combat property wasn't set on joining the battle"
        team = CombatTeam(TeamBuilder().build())
        combat = get_mocked_combat(team)
        self.assertEqual(team.combat, combat, error)

    def test_action_switch_priority(self):
        error = "Switch wasn't faster than a regular ability"
        team_a = CombatTeam(TeamBuilder().build())
        team_b = CombatTeam(TeamBuilder().build())
        combat = get_mocked_combat(team_a, team_b)
        combat_elemental = CombatElemental(ElementalBuilder().build(), team_b)
        combat.request_action(ElementalAction(combat_elemental, Claw(), combat))
        combat.request_action(Switch(team_a, combat_elemental, combat_elemental))
        self.assertIsInstance(combat.previous_round_actions[0], Switch, error)

    def test_switch_target(self):
        error = "Attacks didn't retarget after a switch"
        team_a = CombatTeam(TeamBuilder().build())
        team_b = CombatTeam(TeamBuilder().build())
        combat = get_mocked_combat(team_a, team_b)
        old_target = team_b.active_elemental
        target = CombatElementalBuilder().build()
        combat.request_action(ElementalAction(team_a.active_elemental, Claw(), combat))
        hp_before = target.current_hp
        combat.request_action(Switch(team_b, old_target, target))
        hp_after = target.current_hp
        self.assertLess(hp_after, hp_before, error)

    def test_defend_priority(self):
        error = "Defend wasn't faster than other abilities"
        team_a = CombatTeam(TeamBuilder().build())
        team_b = CombatTeam(TeamBuilder().build())
        combat = get_mocked_combat(team_a, team_b)
        faster = CombatElemental(ElementalBuilder().with_speed(10).build(), team_b)
        team_b.change_active_elemental(faster)
        slower = CombatElemental(ElementalBuilder().with_speed(1).build(), team_a)
        team_a.change_active_elemental(slower)
        combat.request_action(ElementalAction(faster, Claw(), combat))
        combat.request_action(ElementalAction(slower, Defend(), combat))
        self.assertIsInstance(combat.previous_round_actions[0].ability, Defend, error)

    def test_action_speed_priority(self):
        error = "Faster elemental didn't attack first"
        team_a = CombatTeam(TeamBuilder().build())
        team_b = CombatTeam(TeamBuilder().build())
        combat = get_mocked_combat(team_a, team_b)
        slower = CombatElemental(ElementalBuilder().with_level(1).build(), team_a)
        team_a.change_active_elemental(slower)
        faster = CombatElemental(ElementalBuilder().with_level(10).with_nickname('loksy').build(), team_b)
        team_b.change_active_elemental(faster)
        combat.request_action(ElementalAction(slower, Claw(), combat))
        faster_action = ElementalAction(faster, Claw(), combat)
        combat.request_action(faster_action)
        expected = combat.previous_round_actions[0].actor.nickname
        self.assertEqual(expected, faster.nickname, error)

    def test_elemental_exp_gain(self):
        error = "Knocking out an elemental didn't grant exp to player's elementals"
        elemental = ElementalBuilder().with_level(5).build()
        player_team = (TeamBuilder()
                       .with_elementals([elemental])
                       .with_owner(PlayerBuilder().build())
                       .build())
        team_a = CombatTeam(player_team)
        team_b = CombatTeam(TeamBuilder().build())
        get_mocked_combat(team_a, team_b)
        # Nearly fatal damage
        damage = team_b.active_elemental.max_hp - 1
        team_b.active_elemental.receive_damage(damage, team_a.active_elemental)
        exp_before = elemental.current_exp
        team_a.make_move(Claw())
        team_b.make_move(Claw())
        exp_after = elemental.current_exp
        self.assertGreater(exp_after, exp_before, error)

    def test_player_exp_gain(self):
        error = "Knocking out an elemental didn't grant exp to player"
        player = PlayerBuilder().build()
        player_team = TeamBuilder().with_owner(player).build()
        player_team.add_elemental(ElementalBuilder().build())
        team_a = CombatTeam(player_team)
        team_b = CombatTeam(TeamBuilder().build())
        get_mocked_combat(team_a, team_b)
        # Nearly fatal damage
        damage = team_b.active_elemental.max_hp - 1
        team_b.active_elemental.receive_damage(damage, team_a.elementals[0])
        exp_before = player.current_exp
        team_a.make_move(Claw())
        team_b.make_move(Claw())
        exp_after = player.current_exp
        self.assertGreater(exp_after, exp_before, error)

    def test_cast_time_wait(self):
        error = "A spell that requires one turn charge time resolved immediately"
        team_a = CombatTeam(TeamBuilder().build())
        team_b = CombatTeam(TeamBuilder().build())
        get_mocked_combat(team_a, team_b)
        elemental_b = team_b.elementals[0]
        health_before = elemental_b.current_hp
        team_a.handle_cast_time(Castable(ShiningLaser()))
        team_b.make_move(Claw())
        self.assertEqual(elemental_b.current_hp, health_before, error)

    def test_cast_recap(self):
        error = "Recap message was incorrect for a cast time spell"
        team_a = CombatTeam(TeamBuilder().build())
        team_b = CombatTeam(TeamBuilder().build())
        get_mocked_combat(team_a, team_b)
        elemental_a = team_a.elementals[0]
        team_a.handle_cast_time(Castable(ShiningLaser()))
        team_b.make_move(Claw())
        self.assertIn(f'{team_a.active_elemental.name} is shining mightily!!', elemental_a.last_action.recap, error)

    def test_cast_time_resolution(self):
        error = "Casted spell didn't resolve when ready"
        team_a = CombatTeam(TeamBuilder().build())
        team_b = CombatTeam(TeamBuilder().build())
        get_mocked_combat(team_a, team_b)
        elemental_b = team_b.elementals[0]
        health_before = elemental_b.current_hp
        team_b.make_move(Defend())
        team_a.handle_cast_time(Castable(ShiningLaser()))
        team_b.make_move(Claw())
        self.assertLess(elemental_b.current_hp, health_before, error)

    def test_cast_resources(self):
        error = "A casted ability incorrectly consumed mana multiple times"
        team_a = CombatTeam(TeamBuilder().build())
        team_b = CombatTeam(TeamBuilder().build())
        get_mocked_combat(team_a, team_b)
        team_b.make_move(Defend())
        team_a.handle_cast_time(Castable(ShiningLaser()))
        mana_before = team_a.active_elemental.current_mana
        team_b.make_move(Claw())
        mana_after = team_a.active_elemental.current_mana
        # Assert greater for turn start mana regen.
        self.assertGreater(mana_after, mana_before, error)

    def test_channeling_resources(self):
        error = "A channeled ability incorrectly consumed mana across its duration"
        team_a = CombatTeam(TeamBuilder().build())
        team_b = CombatTeam(TeamBuilder().build())
        get_mocked_combat(team_a, team_b)
        team_b.make_move(Defend())
        team_a.make_move(Rampage())
        mana_before = team_a.active_elemental.current_mana
        team_b.make_move(Claw())
        mana_after = team_a.active_elemental.current_mana
        # Assert greater for turn start mana regen.
        self.assertGreater(mana_after, mana_before, error)

    def test_elemental_action(self):
        error = "ElementalAction could incorrectly trigger when the elemental is KOed."
        elemental = ElementalBuilder().build()
        team = TeamBuilder().with_elementals([
            elemental
        ]).build()
        team = CombatTeam(team)
        elemental.receive_damage(10000)
        action = ElementalAction(
            actor=team.elementals[0],
            ability=Claw(),
            combat=Mock()
        )
        self.assertFalse(action.can_execute, error)

    def test_attack_knocked_out(self):
        error = "Attack attempted to resolve even though the opponent was KOed"
        team_a = CombatTeam(TeamBuilder().build())
        team_b = CombatTeam(TeamBuilder().build())
        combat = get_mocked_combat(team_a, team_b)
        team_b.active_elemental.receive_damage(10000, team_a.active_elemental)
        action = ElementalAction(
            actor=team_a.active_elemental,
            ability=Claw(),
            combat=combat
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
            combat=Mock()
        )
        self.assertFalse(action.can_execute, error)

    def test_knockout_grace_turn(self):
        error = "An attack could incorrectly be queued while waiting for a knockout replacement"
        team_a = CombatTeam(TeamBuilder().build())
        team_b = CombatTeam(TeamBuilder().build())
        combat = get_mocked_combat(team_a, team_b)
        team_a.active_elemental.receive_damage(10000, team_b.active_elemental)
        team_b.make_move(Claw())
        self.assertEqual(len(combat.action_requests), 0, error)

    def test_knockout_replacement(self):
        error = "A team whose elemental was knocked out couldn't select a replacement"
        team_a = CombatTeam(TeamBuilder().build())
        combat = get_mocked_combat(team_a)
        team_a.active_elemental.receive_damage(10000, Mock())
        new_active = CombatElementalBuilder().build()
        switch = Switch(
            team=team_a,
            old_active=team_a.active_elemental,
            new_active=new_active
        )
        combat.request_action(switch)
        self.assertEqual(team_a.active_elemental, new_active, error)

    def test_forfeit_combat_end(self):
        error = "Battle didn't end when there were no teams on a side"
        team_a = CombatTeam(TeamBuilder().build())
        combat = get_mocked_combat(team_a)
        combat.forfeit(team_a)
        self.assertFalse(combat.in_progress, error)  # TODO

    def test_forfeit_combat_leave(self):
        error = "Team wasn't removed from the battlefield upon forfeiting"
        team_a = CombatTeam(TeamBuilder().build())
        combat = get_mocked_combat(team_a)
        combat.forfeit(team_a)
        self.assertNotIn(team_a, combat.side_a, error)

    def test_forfeit_clear_combat(self):
        error = "Combat wasn't cleared for the player who left the battle"
        team_a = CombatTeam(TeamBuilder().build())
        combat = get_mocked_combat(team_a)
        combat.forfeit(team_a)
        self.assertFalse(team_a.owner.is_busy, error)
