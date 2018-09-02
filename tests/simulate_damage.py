from unittest.mock import Mock

from src.elemental.ability.abilities.claw import Claw
from src.elemental.ability.damage_calculator import DamageCalculator
from src.elemental.combat_elemental import CombatElemental
from src.elemental.elemental_factory import ElementalInitializer
from src.elemental.species.manapher import Manapher
from src.elemental.species.sithel import Sithel
from src.elemental.status_effect.status_effects.enrage import EnrageEffect


def sim_damage(elemental, opponent, level):
    print(f"=== Level {level} {elemental.name} vs {opponent.name} ===")
    combat_elemental = CombatElemental(elemental, Mock())
    combat_opponent = CombatElemental(opponent, Mock())

    for ability in elemental.available_abilities:
        if ability.attack_power == 0:
            continue
        calculator = DamageCalculator( combat_opponent, combat_elemental, ability)
        calculator.calculate()
        damage_percentage = (calculator.final_damage / combat_opponent.max_hp) * 100
        print(f"{ability.name} total damage:", calculator.final_damage, '-',
              f"({int(damage_percentage)}%", f"of {combat_opponent.nickname}'s {combat_opponent.max_hp} HP)")

    for ability in elemental.available_abilities:
        status_effect = ability.status_effect
        if not status_effect:
            continue
        if status_effect.target_recovery > 0:
            print(f"{status_effect.name} heals for {combat_elemental.max_hp * status_effect.target_recovery} HP.")
        if status_effect.attack_power > 0:
            calculator = DamageCalculator(combat_opponent, combat_elemental, status_effect)
            calculator.calculate()
            damage_percentage = (calculator.final_damage / combat_opponent.max_hp) * 100
            print(f"{status_effect.name} total damage:", calculator.final_damage, '-',
                  f"({int(damage_percentage)}%", f"of {combat_opponent.nickname}'s {combat_opponent.max_hp} HP)")

level = 50
for species in ElementalInitializer.ALL_SPECIES:
    for opponent in ElementalInitializer.ALL_SPECIES:
        elemental = ElementalInitializer.make(species, level)
        opposing_elemental = ElementalInitializer.make(opponent, level)
        sim_damage(elemental, opposing_elemental, level)
