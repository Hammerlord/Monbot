from src.elemental.ability.abilities.black_pinion import BlackPinion
from src.elemental.ability.abilities.blessed_rain import BlessedRain
from src.elemental.ability.abilities.blood_fangs import BloodFangs
from src.elemental.ability.abilities.charge import Charge
from src.elemental.ability.abilities.claw import Claw
from src.elemental.ability.abilities.counter import Counter
from src.elemental.ability.abilities.cyclone import Cyclone
from src.elemental.ability.abilities.defend import Defend
from src.elemental.ability.abilities.deluge import Deluge
from src.elemental.ability.abilities.dissonant_roar import DissonantRoar
from src.elemental.ability.abilities.enrage import Enrage
from src.elemental.ability.abilities.fireball import Fireball
from src.elemental.ability.abilities.frost_barrier import FrostBarrier
from src.elemental.ability.abilities.gale_step import GaleStep
from src.elemental.ability.abilities.geyser import Geyser
from src.elemental.ability.abilities.howling_dark import HowlingDark
from src.elemental.ability.abilities.icy_snap import IcySnap
from src.elemental.ability.abilities.ignite import Ignite
from src.elemental.ability.abilities.quake import Quake
from src.elemental.ability.abilities.rampage import Rampage
from src.elemental.ability.abilities.razor_fangs import RazorFangs
from src.elemental.ability.abilities.reap import Reap
from src.elemental.ability.abilities.recharge import Recharge
from src.elemental.ability.abilities.rend import Rend
from src.elemental.ability.abilities.rolling_thunder import RollingThunder
from src.elemental.ability.abilities.shining_laser import ShiningLaser
from src.elemental.ability.abilities.slam import Slam
from src.elemental.ability.abilities.stone_hide import Stonehide
from src.elemental.ability.abilities.stormbolt import Stormbolt
from src.elemental.ability.abilities.wind_rush import Windrush
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

    @staticmethod
    def gale_step(level=0) -> LearnableAbility:
        return LearnableAbility(GaleStep(), level)

    @staticmethod
    def stormbolt(level=0) -> LearnableAbility:
        return LearnableAbility(Stormbolt(), level)

    @staticmethod
    def geyser(level=0) -> LearnableAbility:
        return LearnableAbility(Geyser(), level)

    @staticmethod
    def ignite(level=0) -> LearnableAbility:
        return LearnableAbility(Ignite(), level)

    @staticmethod
    def windrush(level=0) -> LearnableAbility:
        return LearnableAbility(Windrush(), level)

    @staticmethod
    def black_pinion(level=0) -> LearnableAbility:
        return LearnableAbility(BlackPinion(), level)

    @staticmethod
    def cyclone(level=0) -> LearnableAbility:
        return LearnableAbility(Cyclone(), level)

    @staticmethod
    def deluge(level=0) -> LearnableAbility:
        return LearnableAbility(Deluge(), level)

    @staticmethod
    def rampage(level=0) -> LearnableAbility:
        return LearnableAbility(Rampage(), level)

    @staticmethod
    def quake(level=0) -> LearnableAbility:
        return LearnableAbility(Quake(), level)

    @staticmethod
    def counter(level=0) -> LearnableAbility:
        return LearnableAbility(Counter(), level)

    @staticmethod
    def dissonant_roar(level=0) -> LearnableAbility:
        return LearnableAbility(DissonantRoar(), level)

    @staticmethod
    def howling_dark(level=0) -> LearnableAbility:
        return LearnableAbility(HowlingDark(), level)

    @staticmethod
    def frost_barrier(level=0) -> LearnableAbility:
        return LearnableAbility(FrostBarrier(), level)

    @staticmethod
    def icy_snap(level=0) -> LearnableAbility:
        return LearnableAbility(IcySnap(), level)

    @staticmethod
    def recharge(level=0) -> LearnableAbility:
        return LearnableAbility(Recharge(), level)

    @staticmethod
    def stonehide(level=0) -> LearnableAbility:
        return LearnableAbility(Stonehide(), level)