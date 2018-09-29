import unittest

from src.elemental.ability.abilities.wait import Wait
from src.elemental.ability.ability import Ability
from src.elemental.combat_elemental import CombatElemental
from src.elemental.elemental import Elemental
from tests.elemental.elemental_builder import CombatElementalBuilder, ElementalBuilder


class CombatElementalTests(unittest.TestCase):
    """
    Tests for CombatElemental, the wrapper class generated when an Elemental enters combat.
    """

    def setUp(self):
        self.elemental = self.get_elemental()
        self.combat_elemental = CombatElementalBuilder().with_elemental(self.elemental).build()

    def tearDown(self):
        self.combat_elemental = None
        self.elemental = None

    def get_elemental(self) -> Elemental:
        return ElementalBuilder() \
            .with_current_hp(5) \
            .with_max_hp(50) \
            .build()

    def get_combat_elemental(self) -> CombatElemental:
        return CombatElementalBuilder().with_elemental(self.get_elemental()).build()

    def test_starting_mana(self):
        error = "CombatElemental didn't have the correct amount of starting mana"
        combat_elemental_mana = self.combat_elemental.current_mana
        expected_mana = self.elemental.starting_mana
        self.assertEqual(combat_elemental_mana, expected_mana, error)

    def test_starting_hp(self):
        error = "CombatElemental's HP didn't refer to its Elemental's HP"
        combat_elemental_hp = self.combat_elemental.current_hp
        expected_hp = self.elemental.current_hp
        self.assertEqual(combat_elemental_hp, expected_hp, error)

    def test_defend_charges(self):
        error = "CombatElemental's Defend charges didn't refer to its Elemental's"
        combat_elemental_charges = self.combat_elemental.defend_charges
        min_charges = 2  # All Elementals have at least two Defend charges
        self.assertGreaterEqual(combat_elemental_charges, min_charges, error)

    def test_defend_available(self):
        error = "CombatElemental didn't have defend available as an ability"
        abilities = self.combat_elemental.abilities
        has_defend = any([ability for ability in abilities if ability.name == "Defend"])
        self.assertTrue(has_defend, error)

    def test_defend_unavailable(self):
        error = "Defend was available even though there were no defend charges"
        self.combat_elemental.update_defend_charges(-self.combat_elemental.defend_charges)
        abilities = self.combat_elemental.available_abilities
        has_defend = any([ability for ability in abilities if ability.name == "Defend"])
        self.assertFalse(has_defend, error)

    def test_has_abilities(self):
        error = "CombatElemental doesn't have Abilities"
        abilities = self.combat_elemental.abilities
        self.assertGreater(len(abilities), 0, error)
        self.assertIsInstance(abilities[0], Ability, error)

    def test_bide_available(self):
        error = "Bide wasn't available when there were no other usable abilities"
        self.combat_elemental._abilities = []
        self.assertIsInstance(self.combat_elemental.available_abilities[0], Wait, error)

    def test_bide_unavailable(self):
        error = "Bide shouldn't be available if anything else is available"
        is_bide_available = any([ability for ability in self.combat_elemental.available_abilities
                                 if ability.name == Wait().name])
        self.assertFalse(is_bide_available, error)

    def test_take_damage(self):
        error = "Reference Elemental didn't take damage when CombatElemental took damage"
        prev_hp = self.elemental.current_hp
        self.combat_elemental.receive_damage(2, self.get_combat_elemental())
        current_hp = self.elemental.current_hp
        expected_hp = prev_hp - 2
        self.assertEqual(current_hp, expected_hp, error)

    def test_heal(self):
        error = "Reference Elemental didn't heal when CombatElemental healed"
        prev_hp = self.elemental.current_hp
        self.combat_elemental.heal(5)
        current_hp = self.elemental.current_hp
        expected_hp = prev_hp + 5
        self.assertEqual(current_hp, expected_hp, error)

    def test_stat_change(self):
        error = "Reference Elemental's stats incorrectly changed when CombatElemental's stats changed"
        # TODO

    def test_overkill(self):
        error = "Elemental's HP didn't set to 0 on overkill"
        self.combat_elemental.receive_damage(200, self.get_combat_elemental())
        current_hp = self.elemental.current_hp
        expected_hp = 0
        self.assertEqual(current_hp, expected_hp, error)

    def test_overheal(self):
        error = "Elemental's HP didn't set to max HP on overheal"
        self.combat_elemental.heal(100)
        current_hp = self.elemental.current_hp
        expected_hp = 50
        self.assertEqual(current_hp, expected_hp, error)

    def test_knockout_flag(self):
        error = "CombatElemental wasn't flagged as knocked out at 0 HP"
        self.combat_elemental.receive_damage(12, self.get_combat_elemental())
        knocked_out = self.combat_elemental.is_knocked_out
        self.assertIs(knocked_out, True, error)

    def test_gain_mana(self):
        error = "CombatElemental didn't gain mana on turn start"
        mana_before_turn = self.combat_elemental.current_mana
        self.combat_elemental.start_turn()
        mana_after_turn = self.combat_elemental.current_mana
        self.assertGreater(mana_after_turn, mana_before_turn, error)


