from src.elemental.ability.abilities.blessed_rain import BlessedRain
from src.elemental.ability.abilities.blood_fangs import BloodFangs
from src.elemental.ability.abilities.charge import Charge
from src.elemental.ability.abilities.claw import Claw
from src.elemental.ability.abilities.defend import Defend
from src.elemental.ability.abilities.enrage import Enrage
from src.elemental.ability.abilities.fireball import Fireball
from src.elemental.ability.abilities.razor_fangs import RazorFangs
from src.elemental.ability.abilities.reap import Reap
from src.elemental.ability.abilities.rend import Rend
from src.elemental.ability.abilities.rolling_thunder import RollingThunder
from src.elemental.ability.abilities.shining_laser import ShiningLaser
from src.elemental.ability.abilities.slam import Slam
from src.elemental.ability.ability import LearnableAbility, Ability


class LearnableAbilities:
    """
    Factory for LearnableAbilities. Pass in the level requirement to set a requirement higher than 0.
    """

    @staticmethod
    def defend() -> LearnableAbility:
        return LearnableAbility(Defend())  # Base LearnableAbility has no requirements.

    @staticmethod
    def claw(level=0) -> LearnableAbility:
        return LearnableAbility(Claw(), level)

    @staticmethod
    def charge(level=0) -> LearnableAbility:
        return LearnableAbility(Charge(), level)

    @staticmethod
    def enrage(level=0) -> LearnableAbility:
        return LearnableAbility(Enrage(), level)

    @staticmethod
    def slam(level=0) -> LearnableAbility:
        return LearnableAbility(Slam(), level)

    @staticmethod
    def razor_fangs(level=0) -> LearnableAbility:
        return LearnableAbility(RazorFangs(), level)

    @staticmethod
    def fireball(level=0) -> LearnableAbility:
        return LearnableAbility(Fireball(), level)

    @staticmethod
    def shining_laser(level=0) -> LearnableAbility:
        return LearnableAbility(ShiningLaser(), level)

    @staticmethod
    def rolling_thunder(level=0) -> LearnableAbility:
        return LearnableAbility(RollingThunder(), level)

    @staticmethod
    def blessed_rain(level=0) -> LearnableAbility:
        return LearnableAbility(BlessedRain(), level)

    @staticmethod
    def rend(level=0) -> LearnableAbility:
        return LearnableAbility(Rend(), level)

    @staticmethod
    def blood_fangs(level=0) -> LearnableAbility:
        return LearnableAbility(BloodFangs(), level)

    @staticmethod
    def reap(level=0) -> LearnableAbility:
        return LearnableAbility(Reap(), level)