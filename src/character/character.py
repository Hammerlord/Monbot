import math
from typing import List

from src.character.inventory import Inventory, ItemSlot
from src.elemental.combat_elemental import CombatElemental
from src.elemental.elemental import Elemental
from src.team.team import Team


class Character:
    """
    Base class of NPCs and Players (Discord user avatars).
    """

    def __init__(self):
        self._nickname = 'Anonymous'  # TBD
        self._level = 1
        self._max_level = 50
        self._gold = 0
        self._current_exp = 0
        self._exp_to_level = 10
        self._location = 0  # TODO
        self._team = Team(self)
        self._is_npc = False
        self.__elementals = []
        self._inventory = Inventory()

    @property
    def num_elementals(self) -> int:
        return len(self.__elementals)

    @property
    def elementals(self) -> List[Elemental]:
        """
        :return: All elementals that this Character owns, including those not on their current team.
        """
        return self.__elementals.copy()

    @property
    def nickname(self) -> str:
        return self._nickname

    @nickname.setter
    def nickname(self, name: str) -> None:
        self._nickname = self._validate_nickname(name)

    @property
    def team(self) -> Team:
        return self._team

    @property
    def inventory(self) -> Inventory:
        return self._inventory

    @property
    def level(self) -> int:
        return self._level

    @property
    def current_exp(self) -> int:
        return self._current_exp

    @property
    def exp_to_level(self) -> int:
        return self._exp_to_level

    @property
    def is_npc(self) -> bool:
        return self._is_npc

    @property
    def gold(self) -> int:
        return self._gold

    @property
    def items(self) -> List[ItemSlot]:
        return self.inventory.items

    @property
    def materials(self) -> List[ItemSlot]:
        return self.inventory.materials

    @property
    def consumables(self) -> List[ItemSlot]:
        return self.inventory.consumables

    def use_item(self, item, target: Elemental or CombatElemental) -> bool:
        """
        :return: True if this item was used.
        """
        return self.inventory.use_item(item, target)

    def add_item(self, item, amount=1) -> None:
        self.inventory.add_item(item, amount)

    def add_exp(self, amount: int) -> None:
        if self._is_max_level():
            return
        self._current_exp += amount
        self._check_level_up()

    def update_gold(self, amount: int) -> None:
        self._gold += amount

    def add_elemental(self, elemental: Elemental) -> None:
        elemental.owner = self
        self._team.add_elemental(elemental)
        self.__elementals.append(elemental)

    def _check_level_up(self) -> None:
        while self._current_exp >= self._exp_to_level:
            self._level_up()
            if self._is_max_level():
                return

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
