from src.elemental.ability.abilities.charge import Charge
from src.elemental.ability.abilities.claw import Claw
from src.elemental.ability.abilities.defend import Defend
from src.elemental.ability.ability import LearnableAbility, Ability


class AbilityInitializer:
    ability_map = {}  # Dict {[Ability.name]: Ability}

    @staticmethod
    def initialize(ability) -> Ability:
        AbilityInitializer.ability_map[ability.name] = ability
        return ability


class Abilities:
    """
    An Ability is static information, so all usages refer to the same instance of an Ability.
    """

    @staticmethod
    def get_by_name(ability_name: str) -> Ability or None:
        if ability_name in AbilityInitializer.ability_map:
            return AbilityInitializer.ability_map[ability_name]

    defend = AbilityInitializer.initialize(Defend())
    claw = AbilityInitializer.initialize(Claw())
    charge = AbilityInitializer.initialize(Charge())


class LearnableAbilities:
    """
    Factory for LearnableAbilities. Pass in the level requirement to set a requirement higher than 0.
    """

    @staticmethod
    def defend() -> LearnableAbility:
        return LearnableAbility(Abilities.defend)  # Base LearnableAbility has no requirements.

    @staticmethod
    def claw(level=0) -> LearnableAbility:
        return LearnableAbility(Abilities.claw, level)

    @staticmethod
    def charge(level=0) -> LearnableAbility:
        return LearnableAbility(Abilities.charge, level)
