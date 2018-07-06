import unittest

from src.elemental.ability.ability_factory import Abilities
from src.elemental.ability.damage_calculator import DamageCalculator
from src.elemental.status_effect.status_effects.burns import Burn
from tests.elemental.elemental_builder import CombatElementalBuilder


class AbilityTests(unittest.TestCase):
    def test_charge(self):
        error = "Charge didn't gain a damage bonus against a max health target"
        ability = Abilities.charge
        target = CombatElementalBuilder().build()
        actor = CombatElementalBuilder().build()
        calculator = DamageCalculator(target, actor, ability)
        calculator.calculate()
        self.assertGreater(calculator.bonus_multiplier, 1, error)

    def test_fireball(self):
        error = "Fireball didn't gain a damage bonus on a burning target"
        ability = Abilities.fireball
        target = CombatElementalBuilder().build()
        target.add_status_effect(Burn())
        actor = CombatElementalBuilder().build()
        calculator = DamageCalculator(target, actor, ability)
        calculator.calculate()
        self.assertGreater(calculator.bonus_multiplier, 1, error)