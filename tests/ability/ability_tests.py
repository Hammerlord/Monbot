import unittest
from unittest.mock import Mock, MagicMock

from src.combat.actions.elemental_action import ElementalAction
from src.combat.combat import Combat
from src.elemental.ability.abilities.blood_fangs import BloodFangs
from src.elemental.ability.abilities.charge import Charge
from src.elemental.ability.abilities.cyclone import Cyclone
from src.elemental.ability.abilities.defend import Defend
from src.elemental.ability.abilities.fireball import Fireball
from src.elemental.ability.abilities.razor_fangs import RazorFangs
from src.elemental.ability.abilities.reap import Reap
from src.elemental.ability.damage_calculator import DamageCalculator
from src.elemental.status_effect.status_effects.bleeds import RendEffect
from src.elemental.status_effect.status_effects.burns import Burn
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

    def test_fireball(self):
        error = "Fireball didn't gain a damage bonus on a burning target"
        ability = Fireball()
        target = CombatElementalBuilder().build()
        target.add_status_effect(Burn())
        actor = CombatElementalBuilder().build()
        calculator = DamageCalculator(target, actor, ability)
        calculator.calculate()
        self.assertGreater(calculator.bonus_multiplier, 1, error)

    def test_defend_charge(self):
        error = "Defend didn't use a defend charge"
        elemental = CombatElementalBuilder().build()
        previous_charges = elemental.defend_charges
        ElementalAction(actor=elemental,
                        ability=Defend(),
                        combat=self.get_mocked_combat()
                        ).execute()
        self.assertEqual(elemental.defend_charges, (previous_charges - 1), error)

    def test_mana_consumption(self):
        error = "Mana-consuming ability didn't consume mana"
        elemental = CombatElementalBuilder().build()
        previous_mana = elemental.current_mana
        ElementalAction(actor=elemental,
                        ability=RazorFangs(),
                        combat=self.get_mocked_combat()
                        ).execute()
        self.assertLess(elemental.current_mana, previous_mana, error)

    def test_blood_fangs_healing(self):
        error = "Blood Fangs didn't heal the actor"
        elemental = CombatElementalBuilder().build()
        elemental.receive_damage(10, Mock())
        hp_before = elemental.current_hp
        ElementalAction(actor=elemental,
                        ability=BloodFangs(),
                        combat=self.get_mocked_combat()
                        ).execute()
        hp_after = elemental.current_hp
        self.assertGreater(hp_after, hp_before, error)

    def test_blood_fangs_base_healing(self):
        error = "Blood Fangs didn't recover 10% health baseline"
        elemental = CombatElementalBuilder().build()
        action = ElementalAction(actor=elemental,
                                 ability=BloodFangs(),
                                 combat=self.get_mocked_combat()
                                 ).execute()
        self.assertEqual(0.1, action.total_healing / elemental.max_hp, error)

    def test_blood_fangs_scaled_healing(self):
        error = "Blood Fangs didn't scale with missing health"
        elemental = CombatElementalBuilder().build()
        elemental.receive_damage(20, Mock())
        action = ElementalAction(actor=elemental,
                                 ability=BloodFangs(),
                                 combat=self.get_mocked_combat()
                                 ).execute()
        self.assertGreater(action.total_healing / elemental.max_hp, 0.1, error)

    def test_reap(self):
        error = "Reap didn't scale with debuffs on the target"
        target = CombatElementalBuilder().build()
        target.add_status_effect(RendEffect())
        bonus = Reap().get_bonus_multiplier(target, Mock())
        self.assertGreater(bonus, 1, error)

    def test_cyclone_bonus(self):
        error = "Cyclone didn't deal increasing damage with a consecutive hit"
        elemental = CombatElementalBuilder().build()
        cyclone_action = ElementalAction(actor=elemental,
                                         ability=Cyclone(),
                                         combat=self.get_mocked_combat()
                                         )
        elemental.add_action(cyclone_action)
        bonus = Cyclone().get_bonus_multiplier(Mock(), elemental)
        self.assertGreater(bonus, 1, error)

    @staticmethod
    def get_mocked_combat() -> Combat:
        combat = Combat()
        combat.get_target = MagicMock(return_value=CombatElementalBuilder().build())
        return combat
