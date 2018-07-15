import warnings

from src.core.elements import Category, Effectiveness


class DamageCalculator:
    """
    Requires: Actor, target, ability used.
    Damage calculation is:
    + ability.base_power
    + actor.attack // 3
    - target.damage_reduction percentage
    - target.def // 4
    If same element as ability: +25%
    Elemental weakness/resistance: +/-50%
    Bonus multiplier for a custom condition set by damage source: +x%
    """

    def __init__(self, target, actor, damage_source):
        """
        :param target: The CombatElemental receiving damage.
        :param actor: The CombatElemental who is attacking or who applied the effect.
        :param damage_source: Ability or StatusEffect
        """
        self.actor = actor
        self.target = target
        self.damage_source = damage_source
        self.effectiveness_multiplier = self.__get_effectiveness_multiplier()
        self.same_element_multiplier = self.__get_same_element_multiplier()
        self.bonus_multiplier = self.__get_bonus_multiplier()
        self.raw_damage = 0
        self.damage_blocked = 0
        self.damage_defended = 0
        self.final_damage = 0

    @property
    def is_effective(self) -> bool:
        return self.effectiveness_multiplier > 1

    @property
    def is_resisted(self) -> bool:
        return self.effectiveness_multiplier < 1

    def calculate(self) -> None:
        if self.damage_source.base_power == 0:
            return
        self.raw_damage = self.__get_raw_damage()
        self.damage_blocked = self.__get_damage_blocked()  # From damage_reduction
        self.damage_defended = self.__get_damage_defended()  # From def stats
        final_difference = self.raw_damage - self.damage_blocked - self.damage_defended
        if final_difference < 1:
            self.final_damage = 1
        else:
            self.final_damage = final_difference

    def __get_raw_damage(self):
        raw_damage = self.damage_source.base_power
        raw_damage += self.__get_attack_power()
        raw_damage *= self.effectiveness_multiplier
        raw_damage *= self.same_element_multiplier
        raw_damage *= self.bonus_multiplier
        return raw_damage

    def __get_attack_power(self) -> int:
        # Match the ability to the actor's physical or magic attack.
        if self.damage_source.category == Category.PHYSICAL:
            return self.actor.physical_att // 3
        if self.damage_source.category == Category.MAGIC:
            return self.actor.magic_att // 3
        print("Damage source has no category:", self.damage_source.name)
        return 0

    def __get_same_element_multiplier(self) -> float:
        """
        If the ability has the same element as its user, gain 1.25x damage.
        """
        if self.damage_source.element == self.actor.element:
            return 1.25
        return 1

    def __get_effectiveness_multiplier(self) -> float:
        """
        Check if we have a damage reduction or bonus from ability.element vs target.element.
        Eg. the lightning target is weak to earth, so an earth ability does 1.5x damage and is marked as effective.
        Eg. the wind target is strong to fire, so a fire ability does 0.5x damage and is marked as resisted.
        """
        effectiveness = Effectiveness(self.damage_source.element, self.target.element)
        return effectiveness.calculate_multiplier()

    def __get_bonus_multiplier(self) -> float:
        """
        Check a custom condition on the damage source that may trigger a multiplier bonus.
        :return: 1x, if there was no custom condition or the condition failed.
        """
        return self.damage_source.get_bonus_multiplier(self.target, self.actor)

    def __get_damage_blocked(self) -> int:
        """
        target.damage_reduction is a percentage of damage blocked by the enemy.
        :return: Int damage reduced by damage_reduction.
        """
        return int(self.raw_damage * self.target.damage_reduction)

    def __get_damage_defended(self) -> int:
        """
        Match the target's defensive stat against the incoming ability and return
        Defenses scale worse than attack power.
        :return: Int damage reduced by defenses.
        """
        if self.damage_source.category == Category.PHYSICAL:
            return self.target.physical_att // 4
        if self.damage_source.category == Category.MAGIC:
            return self.target.magic_att // 4
        return 0
