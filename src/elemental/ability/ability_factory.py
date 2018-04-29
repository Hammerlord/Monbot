from src.elemental.ability.abilities.claw import Claw
from src.elemental.ability.abilities.defend import Defend
from src.elemental.ability.ability import LearnableAbility


class AbilityFactory:

    @staticmethod
    def defend() -> LearnableAbility:
        return LearnableAbility(Defend())  # Base LearnableAbility has no requirements.

    @staticmethod
    def claw(level=0) -> LearnableAbility:
        return LearnableAbility(Claw(),
                                level)

