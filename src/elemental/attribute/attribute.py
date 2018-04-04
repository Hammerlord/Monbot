from enum import Enum


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
        self.add_stats()

    @property
    def level(self) -> int:
        return self._current_level

    def reset(self) -> None:
        self._current_level = 0

    def add_stats(self) -> None:
        raise NotImplementedError

    def readd_stats(self) -> None:
        """
        If AttributeManager stats have been reset and need to be recalculated.
        """
        for i in range(self._current_level):
            self.add_stats()


class Ferocity(Attribute):
    def __init__(self, attribute_manager):
        super().__init__(attribute_manager)
        self._stat_type = AttributeType.PHYSICAL_ATT
        self._name = "Ferocity"
        self._description = "Increases physical attack power."

    def add_stats(self):
        self._attribute_manager.add_physical_att(10)


class Attunement(Attribute):
    def __init__(self, attribute_manager):
        super().__init__(attribute_manager)
        self._stat_type = AttributeType.MAGIC_ATT
        self._name = "Attunement"
        self._description = "Increases magic attack power."

    def add_stats(self):
        self._attribute_manager.add_magic_att(10)


class Sturdiness(Attribute):
    def __init__(self, attribute_manager):
        super().__init__(attribute_manager)
        self._stat_type = AttributeType.PHYSICAL_DEF
        self._name = "Sturdiness"
        self._description = "Increases physical defence."

    def add_stats(self):
        self._attribute_manager.add_physical_def(10)


class Resolve(Attribute):
    def __init__(self, attribute_manager):
        super().__init__(attribute_manager)
        self._stat_type = AttributeType.HP
        self._name = "Resolve"
        self._description = "Increases maximum health."

    def add_stats(self):
        self._attribute_manager.add_max_hp(20)


class Resistance(Attribute):
    def __init__(self, attribute_manager):
        super().__init__(attribute_manager)
        self._stat_type = AttributeType.MAGIC_DEF
        self._name = "Resistance"
        self._description = "Increases magic defence."

    def add_stats(self):
        self._attribute_manager.add_magic_def(10)


class Swiftness(Attribute):
    def __init__(self, attribute_manager):
        super().__init__(attribute_manager)
        self._stat_type = AttributeType.SPEED
        self._name = "Swiftness"
        self._description = "Increases speed."

    def add_stats(self):
        self._attribute_manager.add_speed(10)

