import unittest

from src.elemental.ability.abilities.charge import Charge
from src.elemental.ability.damage_calculator import DamageCalculator
from tests.elemental.elemental_builder import CombatElementalBuilder


class AbilityTests(unittest.TestCase):
    def test_charge(self):
        error = "Charge didn't gain a damage bonus against a max health target"
        ability = Charge()
        target = CombatElementalBuilder().build()
        actor = CombatElementalBuilder().build()
        calculator = DamageCalculator(target, actor, ability)
        calculator.calculate()
        self.assertGreater(calculator.bonus_multiplier, 1, error)