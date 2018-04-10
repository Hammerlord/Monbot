from src.elemental.ability.ability import LearnableAbility
from src.elemental.ability.defend import Defend


class AbilityFactory:

    @staticmethod
    def defend() -> LearnableAbility:
        return LearnableAbility(Defend())
