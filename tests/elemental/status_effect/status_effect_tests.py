import unittest
from unittest.mock import Mock

from src.combat.actions.elemental_action import ElementalAction
from src.combat.combat import Combat
from src.elemental.ability.abilities.claw import Claw
from src.elemental.status_effect.status_effects.defend import DefendEffect
from src.elemental.status_effect.status_effects.enrage import EnrageEffect
from src.elemental.status_effect.status_effects.rolling_thunder import RollingThunderEffect
from src.team.combat_team import CombatTeam
from src.team.team import Team
from tests.elemental.elemental_builder import CombatElementalBuilder
from tests.elemental.status_effect.fake_effects import GenericBuff, PermaBuff


class StatusEffectTests(unittest.TestCase):

    def setUp(self):
        self.combat_elemental = CombatElementalBuilder().build()

    def tearDown(self):
        self.combat_elemental = None

    def test_add_status_effect(self):
        error = "StatusEffect couldn't be added"
        self.combat_elemental.add_status_effect(GenericBuff())
        num_effects = self.combat_elemental.num_status_effects
        self.assertEqual(num_effects, 1, error)

    def test_effect_duration_self(self):
        error = "StatusEffect duration wasn't boosted by 1 when self-applied"
        # The duration decrements on turn end, so it loses 1 duration when applied to self.
        buff = EnrageEffect()
        buff.applier = self.combat_elemental
        duration_before = buff.turns_remaining
        self.combat_elemental.add_status_effect(buff)
        duration_after = buff.turns_remaining
        self.assertEqual(duration_after - duration_before, 1, error)

    def test_effect_duration_self_team(self):
        error = "StatusEffect duration wasn't boosted by 1 when applied to own team"
        # The duration decrements on turn end, so it loses 1 duration when applied to self.
        effect = RollingThunderEffect()
        effect.applier = self.combat_elemental
        team = CombatTeam(Team(Mock()))
        team.set_combat(Combat())
        team.change_active_elemental(self.combat_elemental)
        duration_before = effect.turns_remaining
        team.add_status_effect(effect)
        duration_after = effect.turns_remaining
        self.assertEqual(duration_after - duration_before, 1, error)

    def test_effect_duration_decrement(self):
        error = "StatusEffect duration didn't decrement on turn end"
        buff = EnrageEffect()
        self.combat_elemental.add_status_effect(buff)
        duration_before = buff.turns_remaining
        self.combat_elemental.end_turn()
        duration_after = buff.turns_remaining
        self.assertLess(duration_after, duration_before, error)

    def test_effect_end(self):
        error = "StatusEffect wasn't removed upon duration end"
        buff = GenericBuff()
        self.combat_elemental.add_status_effect(buff)
        for i in range(buff.turns_remaining):
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
        duration_before = buff.turns_remaining
        self.combat_elemental.end_turn()
        self.combat_elemental.add_status_effect(same_buff)
        duration_after = buff.turns_remaining
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
        for i in range(buff.turns_remaining):
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
        duration_before = buff.turns_remaining
        self.combat_elemental.end_turn()  # Remove the effect via duration end
        duration_after = buff.turns_remaining
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

    def test_enrage(self):
        error = "Enrage didn't increase damage output"
        before_buff = ElementalAction(self.combat_elemental, Claw(), CombatElementalBuilder().build())
        before_buff.execute()
        self.combat_elemental.add_status_effect(EnrageEffect())
        self.combat_elemental.end_turn()
        self.combat_elemental.start_turn()
        after_buff = ElementalAction(self.combat_elemental, Claw(), CombatElementalBuilder().build())
        after_buff.execute()
        self.assertGreater(after_buff.final_damage, before_buff.final_damage, error)

    def test_defend_fade(self):
        error = "Defend didn't fade on round end"
        defend = DefendEffect()
        self.combat_elemental.add_status_effect(defend)
        self.combat_elemental.end_round()
        num_effects = self.combat_elemental.num_status_effects
        self.assertEqual(num_effects, 0, error)

    def test_defend_duration(self):
        error = "Defend ended prematurely"
        defend = DefendEffect()
        self.combat_elemental.add_status_effect(defend)
        self.combat_elemental.end_turn()
        num_effects = self.combat_elemental.num_status_effects
        self.assertEqual(num_effects, 1, error)

    def test_rolling_thunder_duration(self):
        error = "Rolling Thunder turn duration didn't decrement"
        effect = RollingThunderEffect()
        team = CombatTeam(Team(Mock()))
        team.set_combat(Combat())
        enemy = CombatElementalBuilder().with_team(team).build()
        team.change_active_elemental(enemy)
        team.add_status_effect(effect)
        duration_before = effect.turns_remaining
        team.end_turn()
        duration_after = effect.turns_remaining
        self.assertLess(duration_after, duration_before, error)

    def test_rolling_thunder(self):
        error = "Rolling Thunder did no damage on resolution"
        effect = RollingThunderEffect()
        effect.applier = self.combat_elemental
        team = CombatTeam(Team(Mock()))
        team.set_combat(Combat())
        enemy = CombatElementalBuilder().with_team(team).build()
        team.change_active_elemental(enemy)
        team.add_status_effect(effect)
        health_before = enemy.current_hp
        team.end_turn()
        team.end_turn()
        health_after = enemy.current_hp
        self.assertLess(health_after, health_before, error)