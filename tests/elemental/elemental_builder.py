from unittest.mock import MagicMock

from src.character.player import Player
from src.core.elements import Elements
from src.elemental.attribute.attribute_factory import AttributeFactory
from src.elemental.combat_elemental import CombatElemental
from src.elemental.elemental import Elemental
from src.elemental.species.species import Species
from tests.character.user_builder import UserBuilder
from tests.elemental.species_builder import SpeciesBuilder


class ElementalBuilder:
    def __init__(self):
        self._species = SpeciesBuilder().build()
        self._level = 1
        self._nickname = None
        self._current_hp = None
        self._max_hp = None
        self._rank = 1
        self._starting_mana = None
        self._physical_def = None
        self._speed = None
        user = UserBuilder().build()
        self._owner = Player(user.id, user.name)
        self._owner._level = 60  # Max level, as Elemental levels are restricted by owner level
        self._attribute_manager = AttributeFactory.create_random()

    def with_element(self, element: Elements) -> 'ElementalBuilder':
        self._species = SpeciesBuilder().with_element(element).build()
        return self

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

    def with_nickname(self, nickname: str) -> 'ElementalBuilder':
        self._nickname = nickname
        return self

    def with_starting_mana(self, amount: int) -> 'ElementalBuilder':
        self._starting_mana = amount
        return self

    def with_physical_def(self, amount: int) -> 'ElementalBuilder':
        self._physical_def = amount
        return self

    def with_speed(self, amount: int) -> 'ElementalBuilder':
        self._speed = amount
        return self

    def build(self) -> 'Elemental':
        elemental = Elemental(self._species,
                              self._attribute_manager)
        elemental.level_to(self._level)
        if self._current_hp is not None:
            elemental._current_hp = self._current_hp
        if self._max_hp is not None:
            elemental._max_hp = self._max_hp
        if self._physical_def is not None:
            elemental._physical_def = self._physical_def
        if self._speed is not None:
            elemental._speed = self._speed
        elemental.owner = self._owner
        if self._nickname:
            elemental.nickname = self._nickname
        return elemental


class CombatElementalBuilder:
    def __init__(self):
        self._elemental = ElementalBuilder().build()
        self._team = MagicMock()

    def with_element(self, element: Elements) -> 'CombatElementalBuilder':
        self._elemental = ElementalBuilder().with_element(element).build()
        return self

    def with_elemental(self, elemental: Elemental) -> 'CombatElementalBuilder':
        self._elemental = elemental
        return self

    def with_team(self, team) -> 'CombatElementalBuilder':
        self._team = team
        return self

    def build(self):
        return CombatElemental(self._elemental,
                               self._team)
