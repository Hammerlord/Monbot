import math
import random

from src.core.elements import Category, Effectiveness
from src.elemental.combat_elemental import CombatElemental


class DamageCalculator:
    """
    Requires: Actor, target, ability used.
    Damage calculation is:
    + ability.base_power
    + actor.attack // 3
    - target.damage_reduction percentage
    - target.def // 5
    If same element as ability: +25%
    Elemental weakness/resistance: +/-50%
    """

    def __init__(self, actor: CombatElemental,
                 target: CombatElemental,
                 ability):
        self.actor = actor
        self.target = target
        self.ability = ability
        self.raw_damage = self.get_raw_damage()
        self.damage_reduced = self.get_damage_reduced()
        self.final_damage = 0
        self.is_effective = False
        self.is_resisted = False

    def calculate(self) -> None:
        final_difference = self.raw_damage - self.damage_reduced
        if final_difference < 1:
            self.final_damage = 1
        self.final_damage = final_difference

    def get_raw_damage(self):
        raw_damage = self.ability.base_power
        raw_damage += self.get_attack_power()
        raw_damage += self.check_same_element_bonus(raw_damage)
        raw_damage *= self.get_effectiveness_multiplier()
        return raw_damage

    def get_attack_power(self) -> int:
        # Match the ability to the actor's physical or magic attack.
        if self.ability.category == Category.PHYSICAL:
            return self.actor.physical_att // 3
        if self.ability.category == Category.MAGIC:
            return self.actor.magic_att // 3
        return 0

    def check_same_element_bonus(self, raw_damage: int) -> int:
        """
        If the ability has the same element as its user, gain 1.25x damage.
        """
        if self.ability.element == self.actor.element:
            raw_damage += raw_damage * 0.25
        return raw_damage

    def get_effectiveness_multiplier(self) -> float:
        """
        Check if we have a damage reduction or bonus from ability.element vs target.element.
        Eg. the lightning target is weak to earth, so an earth ability does 1.5x damage and is marked as effective.
        Eg. the wind target is strong to fire, so a fire ability does 0.5x damage and is marked as resisted.
        :return:
        """
        effectiveness = Effectiveness(self.ability.element, self.target.element)
        multiplier = effectiveness.calculate()
        if multiplier < 1:
            self.is_resisted = True
        elif multiplier > 1:
            self.is_effective = True
        return multiplier

    def get_damage_reduced(self) -> int:
        # target.damage_reduction is a percentage of damage blocked by the enemy.
        damage_reduced = self.raw_damage * self.target.damage_reduction
        damage_reduced += self.get_defense_value()
        return int(damage_reduced)

    def get_defense_value(self) -> int:
        # Match the target's defensive stat against the incoming ability.
        # Defenses scale worse than attack power.
        if self.ability.category == Category.PHYSICAL:
            return self.target.physical_att // 4
        if self.ability.category == Category.MAGIC:
            return self.target.magic_att // 4
        return 0
