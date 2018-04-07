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

    @property
    def is_space_available(self) -> bool:
        return len(self._elementals) < self._max_size

    @property
    def size(self) -> int:
        return len(self._elementals)

    def swap(self, slot: int, elemental: Elemental):
        """
        Swap an external Elemental into a slot on the Team.
        """
        if not self._is_valid_slot(slot):
            return
        self._elementals[slot] = elemental

    def add_elemental(self, elemental: Elemental) -> None:
        if not self.is_space_available:
            return
        self._elementals.append(elemental)

    def remove_elemental(self, slot: int) -> None:
        self._elementals.pop(slot)

    def get_elemental(self, position: int) -> Elemental or None:
        return self._elementals[position]

    def reorder(self, first: int, second: int) -> None:
        """
        You can only switch slots if both hold an Elemental.
        """
        try:
            self._elementals[first], self._elementals[second] = self._elementals[second], self._elementals[first]
        except IndexError:
            print("Tried to reorder Elementals, but one or more positions were out of range:", first, second)

    def _is_valid_slot(self, slot: int) -> bool:
        """
        Check if the impending position is a valid slot on the Team.
        """
        return 0 <= slot < self.size
