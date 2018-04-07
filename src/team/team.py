from typing import Type, List

from src.elemental.elemental import Elemental


class Team:
    def __init__(self, owner):
        self._elementals = []  # List[Elemental]
        self._nickname = None
        self._note = None
        self._owner = owner
        self._max_size = 4

    @property
    def elementals(self) -> List[Elemental]:
        """
        :return: A reference to this Team's _elementals
        """
        return self._elementals

    @property
    def owner(self):
        """
        :return: Character or Type[Character]
        """
        return self._owner

    def is_space_available(self) -> bool:
        return len(self._elementals) < self._max_size

    def get_size(self) -> int:
        return len(self._elementals)

    def add_elemental(self, elemental: Elemental) -> None:
        if not self.is_space_available():
            return
        self._elementals.append(elemental)

    def remove_elemental(self, position: int) -> None:
        self._elementals.pop(position)

    def get_elemental(self, position: int) -> Elemental or None:
        try:
            return self._elementals[position]
        except IndexError:
            return None

    def reorder(self, first: int, second: int) -> None:
        try:
            self._elementals[first], self._elementals[second] = self._elementals[second], self._elementals[first]
        except IndexError:
            raise Exception("Tried to swap Team Elemental positions, but one or more was out of range:",
                            first, second)