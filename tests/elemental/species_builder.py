from typing import List

from src.core.elements import Elements
from src.elemental.ability.ability import LearnableAbility, Ability
from src.elemental.species.species import GrowthRate, Species


class StatsBuilder:

    """
    A builder for entities that use the main stats, eg. GrowthRate, Species.
    """

    def __init__(self):
        self._max_hp = 50
        self._physical_att = 10
        self._physical_def = 10
        self._magic_att = 10
        self._magic_def = 10
        self._speed = 10

    def with_max_hp(self, amount: int) -> 'StatsBuilder':
        self._max_hp = amount
        return self

    def with_physical_att(self, amount: int) -> 'StatsBuilder':
        self._physical_att = amount
        return self

    def with_physical_def(self, amount: int) -> 'StatsBuilder':
        self._physical_def = amount
        return self

    def with_magic_att(self, amount: int) -> 'StatsBuilder':
        self._magic_att = amount
        return self

    def with_magic_def(self, amount: int) -> 'StatsBuilder':
        self._magic_def = amount
        return self

    def with_speed(self, amount: int) -> 'StatsBuilder':
        self._speed = amount
        return self

    def build(self) -> GrowthRate:
        growth_rate = GrowthRate()
        growth_rate._max_hp = self._max_hp
        growth_rate._physical_att = self._physical_att
        growth_rate._magic_att = self._magic_att
        growth_rate._physical_def = self._physical_def
        growth_rate._magic_def = self._magic_def
        growth_rate._speed = self._speed
        return growth_rate


class SpeciesBuilder(StatsBuilder):
    def __init__(self):
        super().__init__()
        self._name = "Thefaketofu"
        self._element = Elements.LIGHT
        self._growth_rate = StatsBuilder().build()
        self._abilities = [LearnableAbility(Ability())]

    def with_name(self, name: str) -> 'SpeciesBuilder':
        self._name = name
        return self

    def with_growth_rate(self, growth_rate: GrowthRate) -> 'SpeciesBuilder':
        self._growth_rate = growth_rate
        return self

    def with_abilities(self, abilities: List[LearnableAbility]) -> 'SpeciesBuilder':
        self._abilities = abilities
        return self

    def build(self) -> Species:
        species = Species()
        species._name = self._name
        species._element = self._element
        species._growth_rate = self._growth_rate
        species._learnable_abilities = self._abilities
        species._max_hp = self._max_hp
        species._physical_att = self._physical_att
        species._physical_def = self._physical_def
        species._magic_att = self._magic_att
        species._magic_def = self._magic_def
        species._speed = self._speed
        return species

