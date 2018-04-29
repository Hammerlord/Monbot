import unittest

from src.core.elements import Elements, Category
from src.elemental.ability.damage_calculator import DamageCalculator
from src.elemental.status_effect.status_effects.defend import DefendEffect
from tests.ability.ability_builder import AbilityBuilder
from tests.elemental.elemental_builder import CombatElementalBuilder


class DamageCalculatorTests(unittest.TestCase):

    def test_effective_ability(self):
        multiplier_error = "Super effective ability didn't apply a correct multiplier"
        flag_error = "Super effective ability wasn't flagged as such"
        # Earth is strong against wind
        ability = AbilityBuilder().with_base_power(10).with_element(Elements.EARTH).build()
        target = CombatElementalBuilder().with_element(Elements.WIND).build()
        actor = CombatElementalBuilder().build()
        calculator = DamageCalculator(target, actor, ability)
        calculator.calculate()
        self.assertGreater(calculator.effectiveness_multiplier, 1, multiplier_error)
        self.assertTrue(calculator.is_effective, flag_error)

    def test_block_damage(self):
        error = "Defend didn't block any damage"
        ability = AbilityBuilder().with_base_power(10).build()
        target = CombatElementalBuilder().build()
        target.add_status_effect(DefendEffect())
        actor = CombatElementalBuilder().build()
        calculator = DamageCalculator(target, actor, ability)
        calculator.calculate()
        self.assertGreater(calculator.damage_blocked, 0, error)

    def test_defend_damage(self):
        error = "Defensive stats didn't mitigate any damage"
        ability = AbilityBuilder().with_base_power(10).with_category(Category.PHYSICAL).build()
        target = CombatElementalBuilder().build()
        actor = CombatElementalBuilder().build()
        calculator = DamageCalculator(target, actor, ability)
        calculator.calculate()
        self.assertGreater(calculator.damage_defended, 0, error)

    def test_no_damage(self):
        error = "Ability with no base power somehow did damage"
        ability = AbilityBuilder().with_base_power(0).build()
        target = CombatElementalBuilder().build()
        actor = CombatElementalBuilder().build()
        calculator = DamageCalculator(target, actor, ability)
        calculator.calculate()
        self.assertEqual(calculator.final_damage, 0, error)

    def test_default_bonus_multiplier(self):
        error = "Ability bonus_multiplier didn't resolve to 1 by default"
        ability = AbilityBuilder().build()
        target = CombatElementalBuilder().build()
        actor = CombatElementalBuilder().build()
        calculator = DamageCalculator(target, actor, ability)
        calculator.calculate()
        self.assertEqual(calculator.bonus_multiplier, 1, error)

    def test_same_element_multiplier(self):
        error = "The Ability being the same element as its user should grant a multiplier"
        ability = AbilityBuilder().with_element(Elements.WATER).build()
        target = CombatElementalBuilder().build()
        actor = CombatElementalBuilder().with_element(Elements.WATER).build()
        calculator = DamageCalculator(target, actor, ability)
        calculator.calculate()
        self.assertGreater(calculator.same_element_multiplier, 1, error)