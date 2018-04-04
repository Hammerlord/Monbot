import math
from typing import List

from src.elemental.attribute.attribute import Attribute
from src.elemental.attribute.attribute_manager import AttributeManager
from src.elemental.species import Species, Elements


class Elemental:
    def __init__(self,
                 species: Species,
                 attribute_manager: AttributeManager):
        super().__init__()
        self._species = species  # TBD by descendants
        self._level = 1
        self._id = 0
        self._max_hp = species.max_hp
        self._current_hp = species.max_hp
        self._starting_mana = species.starting_mana
        self._max_mana = species.max_mana
        self._physical_att = species.physical_att
        self._magic_att = species.magic_att
        self._physical_def = species.physical_def
        self._magic_def = species.magic_def
        self._speed = species.speed
        self._defend_potency = 0.6  # Percentage of damage blocked by Defend.
        self._defend_charges = species.defend_charges
        self._current_exp = 0
        self._exp_to_level = 20
        self._owner = None
        self._nickname = species.name
        self._note = None
        self._left_icon = None  # str. This Elemental's emote, facing right.
        self._right_icon = None  # str. This Elemental's emote, facing left.
        self._portrait = None
        self._attribute_manager = attribute_manager

    @property
    def physical_att(self) -> int:
        return self._physical_att + self._attribute_manager.physical_att

    @property
    def magic_att(self) -> int:
        return self._magic_att + self._attribute_manager.magic_att

    @property
    def physical_def(self) -> int:
        return self._physical_def + self._attribute_manager.physical_def

    @property
    def magic_def(self) -> int:
        return self._magic_def + self._attribute_manager.magic_def

    @property
    def speed(self) -> int:
        return self._speed + self._attribute_manager.speed

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
    def current_hp(self) -> int:
        return self._current_hp

    @property
    def max_hp(self) -> int:
        return self._max_hp + self._attribute_manager.max_hp

    @property
    def defend_potency(self) -> float:
        return self._defend_potency + self._attribute_manager.defend_potency

    @property
    def defend_charges(self) -> int:
        return self._defend_charges + self._attribute_manager.defend_charges

    @property
    def attributes(self) -> List[Attribute]:
        return self._attribute_manager.attributes

    def raise_attribute(self, position: int) -> None:
        try:
            self._attribute_manager.raise_attribute(position)
        except IndexError:
            raise Exception("Tried to raise an Attribute, but it was out of bounds:", position)

    def heal(self, amount: int) -> None:
        self._current_hp += amount
        if self._current_hp > self.max_hp:
            self._current_hp = self.max_hp

    def receive_damage(self, amount: int) -> None:
        self._current_hp -= amount
        if self._current_hp < 0:
            self._current_hp = 0

    @property
    def starting_mana(self) -> int:
        return self._starting_mana + self._attribute_manager.starting_mana

    @property
    def current_exp(self) -> int:
        return self._current_exp

    @property
    def exp_to_level(self) -> int:
        return self._exp_to_level

    @property
    def owner(self):
        """
        :return: NPC or Player
        """
        return self._owner

    @owner.setter
    def owner(self, owner):
        """
        :param owner: NPC or Player
        """
        self._owner = owner

    @property
    def rank(self):
        return self._attribute_manager.rank

    def reset_nickname(self):
        self._nickname = self._species.name

    @nickname.setter
    def nickname(self, name: str) -> None:
        self._nickname = self._validate_nickname(name)

    @property
    def note(self) -> str:
        return self._note

    @note.setter
    def note(self, message: str) -> None:
        self._note = self._validate_note(message)

    def reset_note(self) -> None:
        """
        TODO Sets the note based on the Elemental's Attributes.
        """
        pass

    def _check_level_up(self) -> None:
        while self._current_exp >= self._exp_to_level:
            if self._is_level_cap():
                return
            self._level_up()
            self._check_raise_rank()

    def add_exp(self, amount: int) -> None:
        if self._is_level_cap():
            return
        self._current_exp += amount
        self._check_level_up()

    def _level_up(self) -> None:
        self._current_exp -= self._exp_to_level
        self._level += 1
        self._gain_stats()
        self._increase_exp_to_level()

    def _gain_stats(self) -> None:
        """
        Gain stats based on the Species' GrowthRate.
        """
        growth_rate = self._species.growth_rate
        self._max_hp += growth_rate.hp + self._bonus_stat()
        self._physical_att += growth_rate.physical_att + self._bonus_stat()
        self._magic_att += growth_rate.magic_att + self._bonus_stat()
        self._physical_def += growth_rate.physical_def + self._bonus_stat()
        self._magic_def += growth_rate.magic_def + self._bonus_stat()

    def _bonus_stat(self) -> int:
        """
        Every 20 levels, Elemental gains +1 additional of each stat.
        """
        bonus = math.floor(self._level / 20)
        return int(bonus)

    def _check_raise_rank(self) -> None:
        """
        Elementals gain a rank at level 10, 20 ...
        TODO: Item requirements.
        """
        if self._level % 10 == 0:
            self._attribute_manager.raise_rank()

    def _is_level_cap(self) -> bool:
        """
        Elemental can't grow to a higher level than its owner.
        """
        if self._owner:
            return self._level == self._owner.level

    def _increase_exp_to_level(self) -> None:
        self._exp_to_level += math.floor(self._exp_to_level / 10) + 5

    @staticmethod
    def _validate_nickname(name: str) -> str:
        max_length = 15
        name = name.strip()
        if len(name) > max_length:
            return name[:max_length]
        return name

    @staticmethod
    def _validate_note(note: str) -> str:
        max_length = 75
        note = note.strip()
        if len(note) > max_length:
            return note[:max_length]
        return note
