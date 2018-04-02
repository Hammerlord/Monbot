from src.character.character import Character
from src.elemental.elemental import Elemental


class Player(Character):
    def __init__(self, user):
        super().__init__()
        self._is_busy = False
        self._current_interface = None  # TODO
        self.id = user.id
        self._nickname(user.name)

    @staticmethod
    def create_player(user, starter: Elemental) -> 'Player':
        new_profile = Player(user)
        new_profile.add_elemental(starter)
        return new_profile
