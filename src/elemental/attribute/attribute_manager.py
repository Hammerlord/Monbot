from typing import List

from src.data.resources import AttributeResource
from src.elemental.attribute.attribute import Attribute


class AttributeManager:
    """
    Elementals come with three random Attributes. Points can be invested into these Attributes,
    which increase the Elemental's stats and grant other bonuses.
    """

    MAX_NUM_ATTRIBUTES = 3

    def __init__(self):
        self._rank = 1
        self._attributes = []
        self._physical_att = 0
        self._magic_att = 0
        self._physical_def = 0
        self._magic_def = 0
        self._speed = 0
        self._max_hp = 0
        self._defend_potency = 0  # Float. Bonus percentage of damage blocked by Defend.
        self._defend_charges = 0
        self._mana_per_turn = 0
        self._bench_mana_per_turn = 0
        self._starting_mana = 0
        self._max_mana = 0
        self._points_remaining = 0
        self._ferocity = 0
        self._attunement = 0
        self._sturdiness = 0
        self._resolve = 0
        self._resistance = 0
        self._swiftness = 0

    def add_attribute(self, attribute: Attribute) -> None:
        attribute.manager = self
        self._attributes.append(attribute)

    @property
    def ferocity(self) -> int:
        return self._ferocity

    @property
    def attunement(self) -> int:
        return self._attunement

    @property
    def sturdiness(self) -> int:
        return self._sturdiness

    @property
    def resolve(self) -> int:
        return self._resolve

    @property
    def resistance(self) -> int:
        return self._resistance

    @property
    def swiftness(self) -> int:
        return self._swiftness

    @property
    def rank(self) -> int:
        return self._rank

    @property
    def points_remaining(self) -> int:
        return self._points_remaining

    @property
    def attributes(self) -> List[Attribute]:
        return list(self._attributes)

    @property
    def physical_att(self) -> int:
        return self._physical_att

    def add_physical_att(self, amount: int) -> None:
        self._physical_att += amount

    @property
    def magic_att(self) -> int:
        return self._magic_att

    def add_magic_att(self, amount: int) -> None:
        self._magic_att += amount

    @property
    def physical_def(self) -> int:
        return self._physical_def

    def add_physical_def(self, amount: int) -> None:
        self._physical_def += amount

    @property
    def magic_def(self) -> int:
        return self._magic_def

    def add_magic_def(self, amount: int) -> None:
        self._magic_def += amount

    @property
    def speed(self) -> int:
        return self._speed

    def add_speed(self, amount: int) -> None:
        self._speed += amount

    @property
    def max_hp(self) -> int:
        return self._max_hp

    def add_max_hp(self, amount: int) -> None:
        self._max_hp += amount

    @property
    def defend_potency(self) -> int:
        return self._defend_potency

    def add_defend_potency(self, amount: float) -> None:
        self._defend_potency += amount

    @property
    def defend_charges(self) -> int:
        return self._defend_charges

    def add_defend_charges(self, amount: int) -> None:
        self._defend_charges += amount

    @property
    def mana_per_turn(self) -> int:
        return self._mana_per_turn

    def add_mana_per_turn(self, amount: int) -> None:
        self._mana_per_turn += amount

    @property
    def bench_mana_per_turn(self) -> int:
        return self._bench_mana_per_turn

    def add_bench_mana_per_turn(self, amount: int) -> None:
        self._bench_mana_per_turn += amount

    @property
    def starting_mana(self) -> int:
        return self._starting_mana

    def add_starting_mana(self, amount: int) -> None:
        self._starting_mana += amount

    @property
    def max_mana(self) -> int:
        return self._max_mana

    def add_max_mana(self, amount: int) -> None:
        self._max_mana += amount

    def raise_rank(self):
        self._rank += 1
        self._points_remaining += 1

    def raise_attribute(self, attribute: Attribute):
        if self.has_attribute_points and attribute.can_level_up:
            attribute.level_up()
            self._points_remaining -= 1

    def reset_attributes(self) -> None:
        self._reset_stat_bonuses()
        for attribute in self._attributes:
            attribute.reset()
        self._points_remaining = self._rank - 1

    @property
    def has_attribute_points(self) -> bool:
        return self._points_remaining > 0

    def to_server(self) -> List[dict]:
        return [AttributeResource(attribute.name, attribute.level)._asdict()
                for attribute in self.attributes]

    def _reset_stat_bonuses(self):
        self._physical_att = 0
        self._magic_att = 0
        self._physical_def = 0
        self._magic_def = 0
        self._speed = 0
        self._max_hp = 0
        self._defend_potency = 0
        self._defend_charges = 0
        self._mana_per_turn = 0
        self._starting_mana = 0
