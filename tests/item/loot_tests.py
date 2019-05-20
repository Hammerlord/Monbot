import unittest

from src.combat.loot_generator import LootGenerator
from src.elemental.species.npc_monsters.manapher import Manapher
from src.team.combat_team import CombatTeam
from tests.elemental.elemental_builder import ElementalBuilder
from tests.team.team_builder import TeamBuilder


class LootGeneratorTests(unittest.TestCase):
    def wild_elemental_loot(self):
        error = "Wild elemental didn't award loot"
        winning_teams = [CombatTeam(TeamBuilder().build())]
        wild_elemental = ElementalBuilder().with_species(Manapher()).build()  # Manapher has 100% drop rate
        losing_teams = [CombatTeam(TeamBuilder()
                                   .with_elementals([wild_elemental])
                                   .with_owner(None)
                                   .build())]  # Wild elemental teams have no owner
        generator = LootGenerator(winning_teams, losing_teams)
        generator.generate_loot()
        self.assertGreater(len(generator.items_dropped), 0, error)

    def elementalist_money(self):
        error = "Elementalist didn't award money"
        winning_teams = [CombatTeam(TeamBuilder().build())]
        losing_teams = [CombatTeam(TeamBuilder().build())]
        generator = LootGenerator(winning_teams, losing_teams)
        generator.generate_loot()
        self.assertGreater(generator.gold_earned, 0, error)

    def test_victory_elementalist_no_loot(self):
        error = "Elementalist shouldn't award loot"
        winning_teams = [CombatTeam(TeamBuilder().build())]
        wild_elemental = ElementalBuilder().with_species(Manapher()).build()  # Manapher has 100% drop rate
        losing_teams = [CombatTeam(TeamBuilder()
                                   .with_elementals([wild_elemental])
                                   .build())]
        generator = LootGenerator(winning_teams, losing_teams)
        generator.generate_loot()
        self.assertEqual(len(generator.items_dropped), 0, error)
