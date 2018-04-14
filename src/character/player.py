from src.character.character import Character
from src.elemental.elemental_factory import ElementalInitializer


class Player(Character):
    def __init__(self, user):
        super().__init__()
        self._is_busy = False
        self._current_interface = None  # TODO
        self.id = user.id
        self._nickname = user.name

    @property
    def is_busy(self) -> bool:
        return self._is_busy

    @is_busy.setter
    def is_busy(self, set_busy: bool) -> None:
        self._is_busy = set_busy


class NewPlayer:
    """
    Factory for creating new players.
    """

    @staticmethod
    def empty_profile(user) -> 'Player':
        return Player(user)

    @staticmethod
    def create_with_rainatu(user) -> 'Player':
        new_profile = Player(user)
        elemental = ElementalInitializer.rainatu()
        new_profile.add_elemental(elemental)
        return new_profile

    @staticmethod
    def create_with_sithel(user) -> 'Player':
        new_profile = Player(user)
        elemental = ElementalInitializer.sithel()
        new_profile.add_elemental(elemental)
        return new_profile

    @staticmethod
    def create_with_mithus(user) -> 'Player':
        new_profile = Player(user)
        elemental = ElementalInitializer.mithus()
        new_profile.add_elemental(elemental)
        return new_profile