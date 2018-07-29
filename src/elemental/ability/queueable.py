from src.elemental.ability.ability import Ability


class Queueable:
    def decrement_time(self) -> None:
        raise NotImplementedError

    def is_initial_use(self) -> bool:
        raise NotImplementedError

    def has_ended(self) -> bool:
        raise NotImplementedError

    def is_ready(self) -> bool:
        # Can this ability be used?
        raise NotImplementedError


class Channelable(Queueable):
    """
    A wrapper for a channeled ability, which is an ability that
    can activate repeatedly over multiple turns.
    """
    def __init__(self,
                 ability: Ability):
        self.ability = ability
        self.turns_to_channel = ability.base_channel_time

    @property
    def is_ready(self) -> bool:
        # While this is queued, it will be able to trigger repeatedly.
        return True

    @property
    def has_ended(self) -> bool:
        return self.turns_to_channel == 0

    def decrement_time(self) -> None:
        self.turns_to_channel -= 1

    def is_initial_use(self) -> bool:
        return self.turns_to_channel == self.ability.base_channel_time


class Castable(Queueable):
    """
    A wrapper class for an Ability with a charge up time.
    The cast time decrement is handled here.
    """
    def __init__(self,
                 ability: Ability):
        """
        :param ability: The castable ability being used.
        :param elemental: CombatElemental using the ability.
        """
        assert(ability.base_cast_time > 0)  # It better have a cast time!
        self.ability = ability
        self.turns_to_activate = ability.base_cast_time

    @property
    def is_ready(self) -> bool:
        return self.has_ended

    @property
    def has_ended(self) -> bool:
        return self.turns_to_activate == 0

    def decrement_time(self):
        self.turns_to_activate -= 1

    def is_initial_use(self) -> bool:
        return self.turns_to_activate == self.ability.base_cast_time
