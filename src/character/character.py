import copy
import math
from typing import List

from src.character.inventory import Inventory
from src.elemental.elemental import Elemental
from src.team.team import Team


class Character:
    """
    Base class of NPCs and Players (Discord user avatars).
    """

    def __init__(self):
        self._nickname = 'Anonymous'  # TBD
        self._level = 1
        self._max_level = 60
        self._gold = 0
        self._current_exp = 0
        self._exp_to_level = 10
        self._location = 0  # TODO
        self._team = Team()
        self._is_npc = False
        self._elementals = []  # List[Elemental]. All Elementals owned by this Character, including ones not on Team.
        self._inventory = Inventory()

    def get_all_elementals(self) -> List[Elemental]:
        return copy.deepcopy(self._elementals)  # Defensive copy

    def get_nickname(self) -> str:
        return self._nickname

    def set_nickname(self, name: str) -> None:
        self._nickname = self._validate_nickname(name)

    def get_team(self) -> Team:
        return self._team

    def get_inventory(self) -> Inventory:
        return self._inventory

    def get_level(self) -> int:
        return self._level

    def get_current_exp(self) -> int:
        return self._current_exp

    def get_exp_to_level(self) -> int:
        return self._exp_to_level

    def is_npc(self) -> bool:
        return self._is_npc

    def add_exp(self, amount: int) -> None:
        if self._is_max_level():
            return
        self._current_exp += amount
        self._check_level_up()

    def get_gold(self) -> int:
        return self._gold

    def update_gold(self, amount: int) -> None:
        self._gold += amount

    def add_elemental(self, elemental: Elemental) -> None:
        self._team.add_elemental(elemental)
        self._elementals.append(elemental)

    def _check_level_up(self) -> None:
        while self._current_exp >= self._exp_to_level:
            if self._is_max_level():
                return
            self._level_up()

    def _is_max_level(self) -> bool:
        return self._level == self._max_level

    def _level_up(self) -> None:
        self._current_exp -= self._exp_to_level
        self._level += 1
        self._increase_exp_to_level()
        if self._is_max_level():
            self._current_exp = 0

    def _increase_exp_to_level(self) -> None:
        self._exp_to_level += math.floor(self._exp_to_level / 10) + 5

    @staticmethod
    def _validate_nickname(name: str) -> str:
        max_length = 15
        name = name.strip()
        if len(name) > max_length:
            return name[:max_length]
        return name
