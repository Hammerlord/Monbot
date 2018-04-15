from src.character.player import Player
from src.elemental.attribute.attribute_factory import AttributeFactory
from src.elemental.combat_elemental import CombatElemental
from src.elemental.elemental import Elemental
from src.elemental.species.species import Species
from tests.character.test_user import UserBuilder
from tests.elemental.species_builder import SpeciesBuilder


class ElementalBuilder:
    def __init__(self):
        self._species = SpeciesBuilder().build()
        self._level = 1
        self._id = 0
        self._nickname = None
        self._current_hp = 50
        self._max_hp = 50
        self._rank = 1
        self._starting_mana = 15
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

    def with_id(self, id: int) -> 'ElementalBuilder':
        self._id = id
        return self

    def with_nickname(self, nickname: str) -> 'ElementalBuilder':
        self._nickname = nickname
        return self

    def with_starting_mana(self, amount: int) -> 'ElementalBuilder':
        self._starting_mana = amount
        return self

    def build(self) -> 'Elemental':
        elemental = Elemental(self._species,
                              self._attribute_manager)
        elemental._current_hp = self._current_hp
        elemental._max_hp = self._max_hp
        elemental.owner = self._owner
        if self._nickname:
            elemental.nickname = self._nickname
        elemental._id = self._id  # TODO dependency?
        self._level_elemental(elemental)
        return elemental

    def _level_elemental(self, elemental: Elemental) -> None:
        # Because the Elemental actually levels up, this method adds stats to its profile.
        while elemental.level < self._level:
            exp = elemental.exp_to_level
            elemental.add_exp(exp)


class CombatElementalBuilder:
    def __init__(self):
        self._elemental = ElementalBuilder().build()

    def with_elemental(self, elemental: Elemental) -> 'CombatElementalBuilder':
        self._elemental = elemental
        return self

    def build(self):
        return CombatElemental(self._elemental)