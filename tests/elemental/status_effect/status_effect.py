import unittest

from tests.elemental.elemental_builder import CombatElementalBuilder
from tests.elemental.status_effect.test_effects import GenericBuff


class StatusEffectTests(unittest.TestCase):

    def setUp(self):
        self.combat_elemental = CombatElementalBuilder().build()

    def tearDown(self):
        self.combat_elemental = None
        self.elemental = None

    def test_add_status_effect(self):
        error = "StatusEffect couldn't be added"
        self.combat_elemental.add_status_effect(GenericBuff())
        num_effects = self.combat_elemental.num_status_effects
        self.assertEquals(num_effects, 1, error)

    def test_effect_duration_decrement(self):
        error = "StatusEffect duration didn't decrement on turn end"
        buff = GenericBuff()
        self.combat_elemental.add_status_effect(buff)
        duration_before = buff.duration_remaining
        self.combat_elemental.on_turn_end()
        duration_after = buff.duration_remaining
        self.assertLess(duration_after, duration_before, error)

    def test_effect_end(self):
        error = "StatusEffect wasn't removed upon duration ended"
        buff = GenericBuff()
        self.combat_elemental.add_status_effect(buff)
        for i in range(buff.duration_remaining):
            self.combat_elemental.on_turn_end()
        num_effects = self.combat_elemental.num_status_effects
        self.assertEquals(num_effects, 0, error)

