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
        :return: A reference to this Team's Elementals
        """
        return self._elementals

    @property
    def owner(self):
        """
        :return: Player or NPC
        """
        return self._owner

    @property
    def is_space_available(self) -> bool:
        return len(self._elementals) < self._max_size

    @property
    def size(self) -> int:
        return len(self._elementals)

    @property
    def is_all_knocked_out(self) -> bool:
        """
        :return: If all Elementals on the Team have been knocked out (0 HP).
        Game over if true.
        """
        return all(elemental.is_knocked_out for elemental in self.elementals)

    def swap(self, slot: int, elemental: Elemental) -> None:
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
        if not self._is_valid_reorder(first, second):
            return
        self._elementals[first], self._elementals[second] = self._elementals[second], self._elementals[first]

    def _is_valid_reorder(self, first: int, second: int) -> bool:
        return self._is_valid_slot(first) and self._is_valid_slot(second)

    def _is_valid_slot(self, slot: int) -> bool:
        """
        Check if the impending position is a valid slot on the Team.
        """
        return 0 <= slot < self.size
