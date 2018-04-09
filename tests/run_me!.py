import unittest
from typing import Type

from tests.character.character import CharacterTests
from tests.character.npc import NPCTests
from tests.character.player import PlayerTests
from tests.elemental.combat_elemental import CombatElementalTests
from tests.elemental.elemental import ElementalTests
from tests.elemental.status_effect.status_effect import StatusEffectTests
from tests.team.combat_team import CombatTeamTests
from tests.team.team import TeamTests

suites = [CharacterTests,
          NPCTests,
          PlayerTests,
          ElementalTests,
          CombatElementalTests,
          TeamTests,
          CombatTeamTests,
          StatusEffectTests]


def load_test(tests: Type[unittest.TestCase]):
    return unittest.TestLoader().loadTestsFromTestCase(tests)


all_tests = unittest.TestSuite([load_test(suite) for suite in suites])

if __name__ == "__main__":
    unittest.main()
