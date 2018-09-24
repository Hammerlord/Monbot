import unittest
from unittest.mock import Mock, MagicMock

from src.combat.actions.elemental_action import ElementalAction
from src.combat.combat import Combat
from src.elemental.ability.abilities.claw import Claw
from src.elemental.ability.abilities.rampage import Rampage
from src.elemental.status_effect.status_effects.bleeds import RendEffect
from src.elemental.status_effect.status_effects.blessed_rain import BlessedRainEffect
from src.elemental.status_effect.status_effects.chill import Chill
from src.elemental.status_effect.status_effects.defend import DefendEffect
from src.elemental.status_effect.status_effects.enrage import EnrageEffect
from src.elemental.status_effect.status_effects.freeze import Freeze
from src.elemental.status_effect.status_effects.frost_barrier import FrostBarrierEffect
from src.elemental.status_effect.status_effects.provoke import ProvokeEffect
from src.elemental.status_effect.status_effects.rolling_thunder import RollingThunderEffect
from src.elemental.status_effect.status_effects.stonehide import StonehideEffect
from src.elemental.status_effect.status_effects.wind_rush import WindrushEffect
from src.team.combat_team import CombatTeam
from src.team.team import Team
from tests.elemental.elemental_builder import CombatElementalBuilder, ElementalBuilder
from tests.elemental.status_effect.fake_effects import GenericBuff, PermaBuff


class StatusEffectTests(unittest.TestCase):

    def setUp(self):
        self.combat_elemental = CombatElementalBuilder().build()

    def tearDown(self):
        self.combat_elemental = None

    @staticmethod
    def get_stub_combat() -> Combat:
        return Combat(data_manager=Mock())

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
        effect = WindrushEffect()
        effect.applier = self.combat_elemental
        team = CombatTeam(Team(Mock()))
        team.set_combat(self.get_stub_combat())
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
        combat = self.get_stub_combat()
        combat.get_target = MagicMock(return_value=CombatElementalBuilder().build())
        before_buff = ElementalAction(self.combat_elemental, Claw(), combat)
        before_buff._refresh_target()
        before_buff.execute()
        self.combat_elemental.add_status_effect(EnrageEffect())
        self.combat_elemental.end_turn()
        after_buff = ElementalAction(self.combat_elemental, Claw(), combat)
        after_buff._refresh_target()
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
        team.set_combat(self.get_stub_combat())
        enemy = CombatElementalBuilder().with_team(team).build()
        team.change_active_elemental(enemy)
        team.add_status_effect(effect)
        duration_before = effect.rounds_remaining
        team.end_round()
        duration_after = effect.rounds_remaining
        self.assertLess(duration_after, duration_before, error)

    def test_rolling_thunder(self):
        error = "Rolling Thunder did no damage on resolution"
        effect = RollingThunderEffect()
        effect.applier = self.combat_elemental
        team = CombatTeam(Team(Mock()))
        team.set_combat(self.get_stub_combat())
        enemy = CombatElementalBuilder().with_team(team).build()
        team.change_active_elemental(enemy)
        team.add_status_effect(effect)
        health_before = enemy.current_hp
        team.end_round()
        team.end_round()
        health_after = enemy.current_hp
        self.assertLess(health_after, health_before, error)

    def test_blessed_rain(self):
        error = "Blessed Rain didn't heal on turn end"
        team = Team(Mock())
        elemental = ElementalBuilder().build()
        team.add_elemental(elemental)
        combat_team = CombatTeam(team)
        combat_team.set_combat(self.get_stub_combat())
        effect = BlessedRainEffect()
        effect.applier = CombatElementalBuilder().build()
        elemental.receive_damage(10)
        combat_team.change_active_elemental(combat_team.eligible_bench[0])
        combat_team.add_status_effect(effect)
        health_before = elemental.current_hp
        combat_team.end_turn()
        health_after = elemental.current_hp
        self.assertGreater(health_after, health_before, error)

    def test_stonehide_duration(self):
        error = "Stonehide didn't fade upon four consecutive attacks"
        elemental = CombatElementalBuilder().build()
        stonehide = StonehideEffect()
        stonehide.applier = elemental
        elemental.add_status_effect(stonehide)
        for i in range(4):
            elemental.receive_damage(1, Mock())
        self.assertEqual(elemental.num_status_effects, 0, error)

    def test_stonehide_debuff_duration(self):
        error = "Stonehide charge didn't decrement upon receiving damage from a debuff"
        elemental = CombatElementalBuilder().build()
        stonehide = StonehideEffect()
        stonehide.applier = elemental
        elemental.add_status_effect(stonehide)
        rend = RendEffect()
        rend.applier = CombatElementalBuilder().build()
        elemental.add_status_effect(rend)
        elemental.end_turn()
        self.assertEqual(stonehide.charges, 3, error)

    def test_frost_barrier_chill(self):
        error = "Attackers were not chilled by Frost Barrier"
        elemental = CombatElementalBuilder().build()
        frost_barrier = FrostBarrierEffect()
        frost_barrier.applier = elemental
        elemental.add_status_effect(frost_barrier)
        attacker = CombatElementalBuilder().build()
        elemental.on_receive_ability(Claw(), attacker)
        self.assertIsInstance(attacker.status_effects[0], Chill, error)

    def test_chill_state(self):
        error = "A chilled target wasn't flagged as such"
        elemental = CombatElementalBuilder().build()
        elemental.add_status_effect(Chill())
        self.assertTrue(elemental.is_chilled, error)

    def test_chill_freeze(self):
        error = "Target was not frozen after 5 applications of Chill"
        chill = Chill()
        elemental = CombatElementalBuilder().build()
        for i in range(5):
            elemental.add_status_effect(chill)
        self.assertEqual(elemental.num_status_effects, 2, error)

    def test_freeze_state(self):
        error = "Target who was frozen wasn't flagged as such"
        elemental = CombatElementalBuilder().build()
        elemental.add_status_effect(Freeze())
        self.assertTrue(elemental.is_frozen, error)

    def test_freeze_cast_cancel(self):
        error = "Frozen target didn't have its cast cleared"
        elemental = CombatElementalBuilder().build()
        elemental.set_channeling(Rampage())
        elemental.add_status_effect(Freeze())
        self.assertIsNone(elemental.action_queued, error)

    def test_switch_prevention(self):
        error = "Elemental who has been provoked wasn't flagged as such"
        elemental = CombatElementalBuilder().build()
        elemental.add_status_effect(ProvokeEffect())
        self.assertFalse(elemental.can_switch, error)

    def test_provoke_applier_switch(self):
        error = "Provoke didn't clear on opponent changed"
        applier = CombatElementalBuilder().build()
        provoke = ProvokeEffect()
        provoke.applier = applier
        elemental = CombatElementalBuilder().build()
        elemental.add_status_effect(provoke)
        elemental.on_opponent_changed(applier)
        self.assertEqual(0, elemental.num_status_effects, error)
