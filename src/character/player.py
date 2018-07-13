from src.character.character import Character
from src.ui.forms.form import Form


class Player(Character):
    def __init__(self, user):
        super().__init__()
        self._is_busy = False
        self.primary_view = None  # Type: Form
        self.secondary_view = None  # Type: Form (eg. also having a logger open)
        self.id = user.id
        self._nickname = user.name

    def has_elemental(self) -> bool:
        return len(self.elementals) > 0

    def set_primary_view(self, view: Form) -> None:
        self.primary_view = view

    @property
    def view_message(self):
        """
        :return: Discord message object.
        This is how the view actually gets represented in Discord.
        """
        return self.primary_view.discord_message

    @property
    def is_busy(self) -> bool:
        return self._is_busy

    @is_busy.setter
    def is_busy(self, set_busy: bool) -> None:
        self._is_busy = set_busy