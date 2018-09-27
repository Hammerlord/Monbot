import unittest
from unittest.mock import Mock

from src.combat.actions.elemental_action import ElementalAction
from src.combat.combat import Combat
from src.elemental.ability.abilities.claw import Claw
from src.team.combat_team import CombatTeam
from tests.elemental.elemental_builder import ElementalBuilder
from tests.team.team_builder import TeamBuilder


class EventLoggerTests(unittest.TestCase):

    @staticmethod
    def get_mocked_combat() -> Combat:
        return Combat(data_manager=Mock())

    @staticmethod
    def get_combat_team() -> CombatTeam:
        elemental = ElementalBuilder().build()
        team = TeamBuilder().build()
        team.add_elemental(elemental)
        return CombatTeam(team)

    def test_knockout_log(self):
        error = "Event logger didn't receive a log for knockout"
        combat = self.get_mocked_combat()
        team_a = self.get_combat_team()
        team_b = self.get_combat_team()
        combat.join_battle(team_a)
        combat.join_battle(team_b)
        team_a.active_elemental.receive_damage(team_a.active_elemental.max_hp - 1,
                                               team_b.active_elemental)
        combat.request_action(ElementalAction(team_a.active_elemental, Claw(), combat))
        combat.request_action(ElementalAction(team_b.active_elemental, Claw(), combat))
        self.assertIn("was knocked out!", combat.turn_logger.most_recent_log.recap, error)

    def test_get_turn_log_knockout(self):
        error = "Turn logs skipped the most recent log on combat end"
        combat = self.get_mocked_combat()
        team_a = self.get_combat_team()
        team_b = self.get_combat_team()
        combat.join_battle(team_a)
        combat.join_battle(team_b)
        team_a.active_elemental.receive_damage(team_a.active_elemental.max_hp - 1,
                                               team_b.active_elemental)
        combat.request_action(ElementalAction(team_a.active_elemental, Claw(), combat))
        combat.request_action(ElementalAction(team_b.active_elemental, Claw(), combat))
        log_groups = combat.turn_logger.get_turn_logs(0)
        ko_log_exists = False
        for log in log_groups[-1]:
            if "was knocked out!" in log.recap:
                ko_log_exists = True
                break
        self.assertTrue(ko_log_exists, error)