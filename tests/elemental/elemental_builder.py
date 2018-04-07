from src.character.player import Player
from src.core.elements import Elements
from src.elemental.attribute.attribute_factory import AttributeFactory
from src.elemental.elemental import Elemental
from src.elemental.species import Species, GrowthRate
from tests.test_user import UserBuilder



class Ability:
    def __init__(self):
        # Temporary stub
        pass


class TestLearnableAbility:
    def __init__(self):
        super().__init__()
        # Temporary stub
        pass


class StatsBuilder:

    """
    A builder for entities that use the main stats, eg. GrowthRate, Species.
    """

    def __init__(self):
        self._max_hp = 50
        self._physical_att = 1
        self._physical_def = 1
        self._magic_att = 1
        self._magic_def = 1
        self._speed = 1

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
        self._abilities = [TestLearnableAbility(), TestLearnableAbility()]

    def with_name(self, name: str) -> 'SpeciesBuilder':
        self._name = name
        return self

    def with_growth_rate(self, growth_rate: GrowthRate) -> 'SpeciesBuilder':
        self._growth_rate = growth_rate
        return self

    def build(self) -> Species:
        species = Species()
        species._name = self._name
        species._element = self._element
        species._growth_rate = self._growth_rate
        species._abilities = self._abilities
        species._max_hp = self._max_hp
        species._physical_att = self._physical_att
        species._physical_def = self._physical_def
        species._magic_att = self._magic_att
        species._magic_def = self._magic_def
        species._speed = self._speed
        return species


class ElementalBuilder:
    def __init__(self):
        self._species = SpeciesBuilder().build()
        self._level = 1
        self._current_hp = 50
        self._max_hp = 50
        self._rank = 1
        self._owner = Player(UserBuilder().build())
        self._owner._level = 60  # Max level, as Elemental levels are restricted by owner level
        self._attribute_manager = AttributeFactory.create_manager()

    def with_current_hp(self, amount: int) -> 'ElementalBuilder':
        self._current_hp = amount
        return self

    def with_max_hp(self, amount: int) -> 'ElementalBuilder':
        self._max_hp = amount
        return self

    def with_level(self, level: int) -> 'ElementalBuilder':
        self._level = level
        return self

    def with_species(self, species: Species) -> 'ElementalBuilder':
        self._species = species
        return self

    def with_owner(self, owner) -> 'ElementalBuilder':
        self._owner = owner
        return self

    def with_attribute_manager(self, manager) -> 'ElementalBuilder':
        self._attribute_manager = manager
        return self

    def with_rank(self, rank: int) -> 'ElementalBuilder':
        self._rank = rank
        return self

    def build(self) -> 'Elemental':
        elemental = Elemental(self._species,
                              self._attribute_manager)
        elemental._current_hp = self._current_hp
        elemental._max_hp = self._max_hp
        elemental.owner = self._owner
        self._level_elemental(elemental)
        return elemental

    def _level_elemental(self, elemental: Elemental) -> None:
        # Because the Elemental actually levels up, this method adds stats to its profile.
        while elemental.level < self._level:
            exp = elemental.exp_to_level
            elemental.add_exp(exp)
