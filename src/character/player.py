from src.character.character import Character
from src.elemental.elemental_factory import ElementalInitializer


class Player(Character):
    def __init__(self, user):
        super().__init__()
        self._is_busy = False
        self.current_view = None  # Type: Form
        self.id = user.id
        self._nickname = user.name

    @property
    def get_message(self):
        """
        :return: Discord message object.
        """
        return self.current_view.message

    @property
    def is_busy(self) -> bool:
        return self._is_busy

    @property
    def has_elemental(self) -> bool:
        return self.num_elementals > 0

    @is_busy.setter
    def is_busy(self, set_busy: bool) -> None:
        self._is_busy = set_busy