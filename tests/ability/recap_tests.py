from unittest import TestCase
from unittest.mock import MagicMock, Mock

from src.combat.actions.casting import Casting
from src.combat.actions.elemental_action import ElementalAction
from src.combat.combat import Combat
from src.elemental.ability.abilities.claw import Claw
from src.elemental.ability.abilities.rampage import Rampage
from src.elemental.ability.abilities.shining_laser import ShiningLaser
from src.elemental.ability.queueable import Castable
from src.team.combat_team import CombatTeam
from tests.elemental.elemental_builder import CombatElementalBuilder, ElementalBuilder
from tests.team.team_builder import TeamBuilder


class RecapTests(TestCase):

    def test_cast_execution_recap(self):
        error = "Recap for execution of a cast was incorrect"
        combat = Combat(Mock())
        team_a = self.get_combat_team(combat)
        team_b = self.get_combat_team(combat)
        team_a.handle_cast_time(Castable(ShiningLaser()))
        team_b.make_move(Claw())
        team_b.make_move(Claw())
        turn_logs = combat.turn_logger.logs[-2]
        self.assertIn("used Shining Laser!", turn_logs[0].recap, error)
        self.assertIn("used Shining Laser!", turn_logs[1].recap, error)

    def test_channel_recap(self):
        error = "Recap for the execution of a channeled ability was incorrect"
        combat = Combat(Mock())
        team_a = self.get_combat_team(combat)
        team_b = self.get_combat_team(combat)
        team_a.make_move(Rampage())
        team_b.make_move(Claw())
        team_b.make_move(Claw())
        elemental = team_a.active_elemental
        turn_logs = combat.turn_logger.logs[-2]
        self.assertEqual(f"{elemental.nickname}'s Rampage continues!", turn_logs[0].recap, error)
        self.assertEqual(f"{elemental.nickname}'s Rampage continues!", turn_logs[1].recap, error)

    @staticmethod
    def get_mocked_combat() -> Combat:
        combat = Combat(Mock())
        combat.get_target = MagicMock(return_value=CombatElementalBuilder().build())
        return combat

    @staticmethod
    def get_combat_team(combat=None):
        """
        :return: A CombatTeam with an elemental in it.
        """
        team = TeamBuilder().build()
        team.add_elemental(ElementalBuilder().build())
        combat_team = CombatTeam(team)
        if combat:
            combat.join_battle(combat_team)
        return combat_team
