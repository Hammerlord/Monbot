import unittest
from unittest.mock import Mock

from tests.elemental.elemental_builder import CombatElementalBuilder
from tests.elemental.status_effect.fake_effects import GenericBuff, PermaBuff


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
        self.assertEqual(num_effects, 1, error)

    def test_effect_duration_decrement(self):
        error = "StatusEffect duration didn't decrement on turn end"
        buff = GenericBuff()
        self.combat_elemental.add_status_effect(buff)
        duration_before = buff.duration_remaining
        self.combat_elemental.end_turn()
        duration_after = buff.duration_remaining
        self.assertLess(duration_after, duration_before, error)

    def test_effect_end(self):
        error = "StatusEffect wasn't removed upon duration end"
        buff = GenericBuff()
        self.combat_elemental.add_status_effect(buff)
        for i in range(buff.duration_remaining):
            self.combat_elemental.end_turn()
        num_effects = self.combat_elemental.num_status_effects
        self.assertEqual(num_effects, 0, error)

    def test_unstackable_effect(self):
        error = "A !can_add_instances StatusEffect incorrectly added multiple instances"
        self.combat_elemental.add_status_effect(GenericBuff())
        self.combat_elemental.add_status_effect(GenericBuff())
        num_effects = self.combat_elemental.num_status_effects
        self.assertEqual(num_effects, 1, error)

    def test_unstackable_effect_refresh(self):
        error = "A !can_add_instances StatusEffect didn't refresh its effect's duration when reapplied"
        buff = GenericBuff()
        same_buff = GenericBuff()
        self.combat_elemental.add_status_effect(buff)
        duration_before = buff.duration_remaining
        self.combat_elemental.end_turn()
        self.combat_elemental.add_status_effect(same_buff)
        duration_after = buff.duration_remaining
        self.assertEqual(duration_before, duration_after, error)

    def test_effect_stats(self):
        error = "Physical attack StatusEffect didn't add any physical attack"
        physical_att_before = self.combat_elemental.physical_att
        buff = GenericBuff()
        self.combat_elemental.add_status_effect(buff)
        physical_att_after = self.combat_elemental.physical_att
        self.assertGreater(physical_att_after, physical_att_before, error)

    def test_effect_stats_end(self):
        error = "Stats change persisted even after the effect ended"
        physical_att_before = self.combat_elemental.physical_att
        buff = GenericBuff()
        self.combat_elemental.add_status_effect(buff)
        for i in range(buff.duration_remaining):
            self.combat_elemental.end_turn()  # Remove the effect via duration end
        physical_att_after = self.combat_elemental.physical_att
        self.assertEqual(physical_att_before, physical_att_after, error)

    def test_effect_stats_consistency(self):
        error = "Stats gained from a buff incorrectly changed across its duration"
        buff = GenericBuff()
        self.combat_elemental.add_status_effect(buff)
        physical_att_before = self.combat_elemental.physical_att
        self.combat_elemental.end_turn()  # Remove the effect via duration end
        physical_att_after = self.combat_elemental.physical_att
        self.assertEqual(physical_att_before, physical_att_after, error)

    def test_perma_buff(self):
        error = "A StatusEffect with no duration could incorrectly be decremented"
        buff = PermaBuff()
        self.combat_elemental.add_status_effect(buff)
        duration_before = buff.duration_remaining
        self.combat_elemental.end_turn()
        duration_after = buff.duration_remaining
        self.assertEqual(duration_after, duration_before, error)

    def test_dispellable_buff(self):
        error = "A dispellable effect could not be dispelled"
        buff = GenericBuff()
        self.combat_elemental.add_status_effect(buff)
        self.combat_elemental.dispel_all(self.combat_elemental)
        num_effects = self.combat_elemental.num_status_effects
        self.assertEqual(num_effects, 0, error)

    def test_undispellable_buff(self):
        error = "An undispellable effect was incorrectly able to be dispelled"
        buff = PermaBuff()
        self.combat_elemental.add_status_effect(buff)
        self.combat_elemental.dispel_all(self.combat_elemental)
        num_effects = self.combat_elemental.num_status_effects
        self.assertEqual(num_effects, 1, error)

    def test_effect_knocked_out(self):
        error = "Status effect wasn't removed when the elemental was knocked out"
        buff = GenericBuff()
        self.combat_elemental.add_status_effect(buff)
        self.combat_elemental.receive_damage(100000, Mock())
        num_effects = self.combat_elemental.num_status_effects
        self.assertEqual(num_effects, 0, error)