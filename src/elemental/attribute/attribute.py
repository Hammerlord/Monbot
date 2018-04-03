from enum import Enum

from src.elemental.attribute.attribute_manager import AttributeManager


class AttributeType(Enum):
    NONE = 0
    PHYSICAL_ATT = 1
    MAGIC_ATT = 2
    PHYSICAL_DEF = 3
    MAGIC_DEF = 4
    SPEED = 5
    HP = 6
    MANA = 7


class Attribute:
    def __init__(self, attribute_manager: 'AttributeManager'):
        self._stat_type = AttributeType.NONE
        self._attribute_manager = attribute_manager
        self._name = None  # Str. TBD by descendants.
        self._description = None  # Str. TBD by descendants.
        self._current_level = 0
        self._max_level = 3

    def can_level_up(self) -> bool:
        return self._current_level < self._max_level

    def level_up(self) -> None:
        self._current_level += 1

    @property
    def level(self) -> int:
        return self._current_level

    def reset(self) -> None:
        self._current_level = 0


class Ferocity(Attribute):
    def __init__(self, attribute_manager):
        self._stat_type = AttributeType.PHYSICAL_ATT
        super().__init__(attribute_manager)
        self._name = "Ferocity"
        self._description = "Increases physical attack power."

    def level_up(self):
        super().level_up()
        self._attribute_manager.add_physical_att(10)

