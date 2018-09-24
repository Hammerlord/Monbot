class Attribute:

    """
    Each Elemental has three random Attributes, which can be ranked up to gain stats and unlock abilities.
    """
    MAX_LEVEL = 5

    def __init__(self):
        self.name = None  # Str. TBD by descendants.
        self.description = None  # Str. TBD by descendants.
        self._current_level = 0
        self.manager = None  # TBD when added to an AttributeManager.

    @property
    def level(self) -> int:
        return self._current_level

    @property
    def total_stat_gain(self) -> int:
        """
        The amount of stats gained by this Attribute.
        """
        raise NotImplementedError

    @property
    def base_stat_gain(self) -> int:
        """
        The amount of stats gained for a particular level.
        """
        return 7 + self.level

    @property
    def can_level_up(self) -> bool:
        return self._current_level < Attribute.MAX_LEVEL

    def level_up(self) -> None:
        self._current_level += 1
        self.add_stats()

    def reset(self) -> None:
        self._current_level = 0

    def add_stats(self) -> None:
        raise NotImplementedError

    def level_to(self, level: int) -> None:
        while self._current_level < int(level):
            if not self.can_level_up:
                return
            self.level_up()


class Ferocity(Attribute):
    def __init__(self):
        super().__init__()
        self.name = "Ferocity"
        self.description = "Physical Attack"

    def add_stats(self) -> None:
        self.manager.add_physical_att(self.base_stat_gain)

    def total_stat_gain(self) -> int:
        return self.manager.physical_att


class Attunement(Attribute):
    def __init__(self):
        super().__init__()
        self.name = "Attunement"
        self.description = "Magic Attack"

    def add_stats(self) -> None:
        self.manager.add_magic_att(self.base_stat_gain)

    def total_stat_gain(self) -> int:
        return self.manager.magic_att


class Sturdiness(Attribute):
    def __init__(self):
        super().__init__()
        self.name = "Sturdiness"
        self.description = "Physical Defence"

    def add_stats(self) -> None:
        self.manager.add_physical_def(self.base_stat_gain)

    def total_stat_gain(self) -> int:
        return self.manager.physical_def


class Resolve(Attribute):
    def __init__(self):
        super().__init__()
        self.name = "Resolve"
        self.description = "Max HP"

    def add_stats(self) -> None:
        self.manager.add_max_hp(self.base_stat_gain)

    def total_stat_gain(self) -> int:
        return self.manager.max_hp


class Resistance(Attribute):
    def __init__(self):
        super().__init__()
        self.name = "Resistance"
        self.description = "Magic Defence"

    def add_stats(self) -> None:
        self.manager.add_magic_def(self.base_stat_gain)

    def total_stat_gain(self) -> int:
        return self.manager.magic_def


class Swiftness(Attribute):
    def __init__(self):
        super().__init__()
        self.name = "Swiftness"
        self.description = "Speed"

    def add_stats(self) -> None:
        self.manager.add_speed(self.base_stat_gain)

    def total_stat_gain(self) -> int:
        return self.manager.speed
