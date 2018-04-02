import math

from src.elemental.species import StatsInterface, Species, Elements


class Elemental:
    def __init__(self, species: Species):
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
        self._defend_potency = 0.5  # float. Percentage of damage blocked by Defend.
        self._current_exp = 0
        self._exp_to_level = 20
        self._owner = None
        self._nickname = None
        self._note = None
        self._left_icon = None  # str. This Elemental's emote, facing right.
        self._right_icon = None  # str. This Elemental's emote, facing left.
        self._portrait = None
        self._attributes = AttributeFactory.build_manager()

    @property
    def physical_att(self) -> int:
        return self._physical_att + self._attributes.physical_att

    @property
    def magic_att(self) -> int:
        return self._magic_att + self._attributes.magic_att

    @property
    def physical_def(self) -> int:
        return self._physical_def + self._attributes.physical_def

    @property
    def magic_def(self) -> int:
        return self._magic_def + self._attributes.magic_def

    @property
    def speed(self) -> int:
        return self._speed + self._attributes.speed

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
        return self._max_hp + self._attributes.max_hp

    @property
    def starting_mana(self) -> int:
        return self._starting_mana + self._attributes.starting_mana

    @property
    def owner(self):
        """
        :return: NPC or Player
        """
        return self._owner

    @property
    def rank(self):
        return self._attributes.rank

    def raise_rank(self) -> None:
        self._attributes.raise_rank()

    def reset_nickname(self):
        self._nickname = self._species.name

    @nickname.setter
    def nickname(self, name: str) -> None:
        self._nickname = self._validate_nickname(name)

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

    def add_exp(self, amount: int) -> None:
        if self._is_level_cap():
            return
        self._current_exp += amount
        self._check_level_up()

    def _level_up(self) -> None:
        self._current_exp -= self._exp_to_level
        self._level += 1
        self._increase_exp_to_level()

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
        max_length = 60
        note = note.strip()
        if len(note) > max_length:
            return note[:max_length]
        return note
