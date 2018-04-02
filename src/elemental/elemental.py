from typing import Type

from src.elemental.species import StatsInterface, Species, Elements


class Elemental(StatsInterface):
    def __init__(self, species: Species):
        super().__init__()
        self._species = species  # TBD by descendants
        self._level = 1
        self._id = 0
        self._max_hp = species.max_hp
        self._current_hp = species.max_hp
        self._starting_mana = species.starting_mana
        self._max_mana = species.max_mana
        self._defend_potency = 0.5  # float. Percentage of damage blocked by Defend.
        self._owner = None
        self._nickname = None
        self._note = None
        self._left_icon = None  # str. This Elemental's emote, facing right.
        self._right_icon = None  # str. This Elemental's emote, facing left.
        self._portrait = None
        self._attributes = AttributeFactory.build_manager()

    @property
    def level(self) -> int:
        return self._level

    @property
    def nickname(self) -> str:
        return self._nickname

    @property
    def element(self) -> Elements:
        return self._species.element

    @property
    def owner(self) -> Type['Character'] or None:
        return self._owner

    def reset_nickname(self):
        self._nickname = self._species.name

    @nickname.setter
    def nickname(self, name: str) -> None:
        self._nickname = self._validate_nickname(name)

    def get_max_level(self) -> int:
        if self._owner:
            return self._owner.get_max_level()

    def reset_note(self) -> None:
        """
        TODO Sets the note based on the Elemental's Attributes.
        """
        pass

    @staticmethod
    def _validate_nickname(name: str) -> str:
        max_length = 15
        name = name.strip()
        if len(name) > max_length:
            return name[:max_length]
        return name

    @staticmethod
    def _validate_note(note: str) -> str:
        max_length = 60
        note = note.strip()
        if len(note) > max_length:
            return note[:max_length]
        return note
