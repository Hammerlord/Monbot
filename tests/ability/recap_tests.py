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
from tests.character.character_builder import PlayerBuilder
from tests.elemental.elemental_builder import CombatElementalBuilder, ElementalBuilder
from tests.team.team_builder import TeamBuilder


def make_combat_team() -> CombatTeam:
    return CombatTeam([ElementalBuilder().build()], PlayerBuilder().build())


class RecapTests(TestCase):

    def test_cast_execution_recap(self):
        error = "Recap for execution of a cast was incorrect"
        team_a = make_combat_team()
        team_b = make_combat_team()
        combat = Combat([team_a], [team_b], Mock())
        team_a.handle_cast_time(Castable(ShiningLaser()))
        team_b.make_move(Claw())
        team_b.make_move(Claw())
        turn_logs = combat.turn_logger.logs[-2]
        self.assertIn("used Shining Laser!", turn_logs[0].recap, error)
        self.assertIn("used Shining Laser!", turn_logs[1].recap, error)

    def test_channel_recap(self):
        error = "Recap for the execution of a channeled ability was incorrect"
        team_a = make_combat_team()
        team_b = make_combat_team()
        combat = Combat([team_a], [team_b], Mock())
        team_a.make_move(Rampage())
        team_b.make_move(Claw())
        team_b.make_move(Claw())
        elemental = team_a.active_elemental
        turn_logs = combat.turn_logger.logs[-2]
        self.assertEqual(f"{elemental.nickname}'s Rampage continues!", turn_logs[0].recap, error)
        self.assertEqual(f"{elemental.nickname}'s Rampage continues!", turn_logs[1].recap, error)