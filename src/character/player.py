from src.character.character import Character
from src.character.consumables import Peach, Revive
from src.ui.forms.form import Form


class Player(Character):
    def __init__(self, user):
        super().__init__()
        self._level = 3
        self._is_busy = False
        self.primary_view = None  # Type: Form
        self.secondary_view = None  # Type: Form (eg. also having a logger open)
        self.id = user.id
        self._nickname = user.name
        self.battles_fought = 0
        self.inventory.add_item(Peach(), 2)
        self.inventory.add_item(Revive(), 1)

    @property
    def can_battle(self) -> bool:
        return not self.team.is_all_knocked_out

    def has_item(self, item) -> bool:
        return self.inventory.has_item(item)

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
