import unittest

from math import floor

from src.items.consumables import Peach, Revive, Cake, Meat, Pudding
from tests.elemental.elemental_builder import ElementalBuilder


class ConsumableTests(unittest.TestCase):
    def test_peach_heal(self):
        elemental = ElementalBuilder().build()
        elemental.receive_damage(elemental.max_hp - 1)
        Peach.use_on(elemental)
        self.assertAlmostEquals(elemental.current_hp, floor(Peach.healing_percentage * elemental.max_hp + 1))

    def test_peach_grants_exp(self):
        elemental = ElementalBuilder().build()
        exp_before = elemental.current_exp
        level_before = elemental.level
        Peach.use_on(elemental)
        self.assertTrue(exp_before < elemental.current_hp or level_before < elemental.level)

    def test_peach_not_usable_on_KO(self):
        elemental = ElementalBuilder().build()
        elemental.receive_damage(elemental.max_hp)
        self.assertFalse(Peach.is_usable_on(elemental))

    def test_revive_usable_on_KO(self):
        elemental = ElementalBuilder().build()
        elemental.receive_damage(elemental.max_hp)
        self.assertTrue(Revive.is_usable_on(elemental))

    def test_revive_heal(self):
        elemental = ElementalBuilder().build()
        elemental.receive_damage(elemental.max_hp)
        Revive.use_on(elemental)
        self.assertAlmostEquals(elemental.current_hp, Revive.healing_percentage * elemental.max_hp)

    def test_cake_heal(self):
        elemental = ElementalBuilder().build()
        elemental.receive_damage(elemental.max_hp - 1)
        Cake.use_on(elemental)
        self.assertAlmostEquals(elemental.current_hp, floor(Cake.healing_percentage * elemental.max_hp + 1))

    def test_cake_grants_exp(self):
        elemental = ElementalBuilder().build()
        exp_before = elemental.current_exp
        Cake.use_on(elemental)
        self.assertGreater(elemental.current_exp, exp_before)

    def test_cake_not_usable_on_KO(self):
        elemental = ElementalBuilder().build()
        elemental.receive_damage(elemental.max_hp)
        self.assertFalse(Cake.is_usable_on(elemental))

    def test_meat_heal(self):
        elemental = ElementalBuilder().build()
        elemental.receive_damage(elemental.max_hp - 1)
        hp_before = elemental.current_hp
        Pudding.use_on(elemental)
        self.assertGreater(elemental.current_hp, hp_before)

    def test_meat_grants_exp(self):
        elemental = ElementalBuilder().build()
        exp_before = elemental.current_exp
        level_before = elemental.level
        Meat.use_on(elemental)
        self.assertTrue(exp_before < elemental.current_hp or level_before < elemental.level)

    def test_meat_not_usable_on_KO(self):
        elemental = ElementalBuilder().build()
        elemental.receive_damage(elemental.max_hp)
        self.assertFalse(Meat.is_usable_on(elemental))

    def test_pudding_heal(self):
        elemental = ElementalBuilder().build()
        elemental.receive_damage(elemental.max_hp - 1)
        hp_before = elemental.current_hp
        Pudding.use_on(elemental)
        self.assertGreater(elemental.current_hp, hp_before)

    def test_pudding_grants_exp(self):
        elemental = ElementalBuilder().build()
        exp_before = elemental.current_exp
        level_before = elemental.level
        Pudding.use_on(elemental)
        self.assertTrue(exp_before < elemental.current_hp or level_before < elemental.level)

    def test_pudding_not_usable_on_KO(self):
        elemental = ElementalBuilder().build()
        elemental.receive_damage(elemental.max_hp)
        self.assertFalse(Pudding.is_usable_on(elemental))