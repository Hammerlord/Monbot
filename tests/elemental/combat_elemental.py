import unittest

from src.elemental.elemental_builder import ElementalBuilder


class CombatElementalTests(unittest.TestCase):
    """
    Tests for CombatElemental, the wrapper class generated when an Elemental enters combat.
    """

    def setUp(self):
        self.elemental = ElementalBuilder() \
            .with_current_hp(5) \
            .with_max_hp(50) \
            .build()
        self.combat_elemental = CombatElementalBuilder() \
            .with_elemental(self.elemental) \
            .build()

    def tearDown(self):
        self.combat_elemental.dispose()
        self.elemental.dispose()
        self.combat_elemental = None
        self.elemental = None

    def test_starting_mana(self):
        error = "CombatElemental didn't have the correct amount of starting mana"
        combat_elemental_mana = self.combat_elemental.get_current_mana()
        expected_mana = self.elemental.get_starting_mana()
        self.assertEqual(combat_elemental_mana, expected_mana, error)

    def test_starting_hp(self):
        error = "CombatElemental's HP didn't refer to its Elemental's HP"
        combat_elemental_hp = self.combat_elemental.get_current_hp()
        expected_hp = self.elemental.get_current_hp()
        self.assertEqual(combat_elemental_hp, expected_hp, error)

    def test_defend_charges(self):
        error = "CombatElemental's Defend charges didn't refer to its Elemental's"
        combat_elemental_charges = self.combat_elemental.get_defend_charges()
        min_charges = 2  # All Elementals have at least two Defend charges
        self.assertGreaterEqual(combat_elemental_charges, min_charges, error)

    def test_has_abilities(self):
        error = "CombatElemental doesn't have Abilities"
        abilities = self.combat_elemental.get_abilities()
        self.assertGreater(len(abilities), 0, error)
        self.assertIsInstance(abilities[0], Ability, error)

    def test_has_status_manager(self):
        error = "CombatElemental didn't instantiate a StatusManager"
        manager = self.combat_elemental.status_effects
        self.assertIsInstance(manager, StatusManager, error)

    def test_take_damage(self):
        error = "Reference Elemental didn't take damage when CombatElemental took damage"
        self.combat_elemental.receive_damage(2)
        current_hp = self.elemental.get_current_hp()
        expected_hp = 3
        self.assertEqual(current_hp, expected_hp, error)

    def test_heal(self):
        error = "Reference Elemental didn't heal when CombatElemental healed"
        self.combat_elemental.heal(5)
        current_hp = self.elemental.get_current_hp()
        expected_hp = 10
        self.assertEqual(current_hp, expected_hp, error)

    def test_stat_change(self):
        error = "Reference Elemental's stats incorrectly changed when CombatElemental's stats changed"
        # TODO

    def test_overkill(self):
        error = "Elemental's HP didn't set to 0 on overkill"
        self.combat_elemental.receive_damage(12)
        current_hp = self.elemental.get_current_hp()
        expected_hp = 0
        self.assertEqual(current_hp, expected_hp, error)

    def test_overheal(self):
        error = "Elemental's HP didn't set to max HP on overheal"
        self.combat_elemental.heal(100)
        current_hp = self.elemental.get_current_hp()
        expected_hp = 50
        self.assertEqual(current_hp, expected_hp, error)

    def test_knockout_flag(self):
        error = "CombatElemental wasn't flagged as knocked out at 0 HP"
        self.combat_elemental.receive_damage(12)
        knocked_out = self.combat_elemental.is_knocked_out()
        self.assertIs(knocked_out, True, error)

    def test_can_switch_flag(self):
        error = "Flag for switch availability could not be set on CombatElemental"
        self.combat_elemental.set_switchable(False)
        self.assertIs(self.combat_elemental.can_switch, False, error)

    def test_gain_mana(self):
        error = "CombatElemental didn't gain mana on turn start"
        mana_before_turn = self.combat_elemental.get_current_mana
        self.combat_elemental.on_turn_start()
        mana_after_turn = self.combat_elemental.get_current_mana
        self.assertGreater(mana_after_turn, mana_before_turn, error)


