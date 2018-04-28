from src.elemental.ability.abilities.defend import Defend
from src.elemental.ability.ability import LearnableAbility


class AbilityFactory:

    @staticmethod
    def defend() -> LearnableAbility:
        return LearnableAbility(Defend())
