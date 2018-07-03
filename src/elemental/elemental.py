import math
import uuid
from typing import List

from src.core.elements import Elements
from src.elemental.ability.ability import Ability
from src.elemental.ability.ability_manager import AbilityManager
from src.elemental.attribute.attribute import Attribute
from src.elemental.attribute.attribute_manager import AttributeManager
from src.elemental.species.species import Species


class Elemental:
    def __init__(self,
                 species: Species,
                 attribute_manager: AttributeManager):
        super().__init__()
        self._species = species  # TBD by descendants
        self._level = 1
        self._id = uuid.uuid4().int  # TODO this is a dependency
        self._max_hp = species.max_hp
        self._current_hp = species.max_hp
        self._starting_mana = species.starting_mana
        self._max_mana = species.max_mana
        self._physical_att = species.physical_att
        self._magic_att = species.magic_att
        self._physical_def = species.physical_def
        self._magic_def = species.magic_def
        self._mana_per_turn = species.mana_per_turn
        self._bench_mana_per_turn = species.bench_mana_per_turn
        self._speed = species.speed
        self._defend_potency = 0.6  # Percentage of damage blocked by Defend.
        self._defend_charges = species.defend_charges
        self._current_exp = 0
        self._exp_to_level = 20
        self._owner = None
        self._nickname = species.name
        self._note = None
        self._attribute_manager = attribute_manager
        self._ability_manager = AbilityManager(self)

    @property
    def left_icon(self) -> str:
        return self._species.left_icon

    @property
    def right_icon(self) -> str:
        return self._species.right_icon

    @property
    def species(self) -> Species:
        return self._species

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
    def ferocity(self) -> int:
        return self._attribute_manager.ferocity

    @property
    def attunement(self) -> int:
        return self._attribute_manager.attunement

    @property
    def sturdiness(self) -> int:
        return self._attribute_manager.sturdiness

    @property
    def resolve(self) -> int:
        return self._attribute_manager.resolve

    @property
    def resistance(self) -> int:
        return self._attribute_manager.resistance

    @property
    def swiftness(self) -> int:
        return self._attribute_manager.swiftness

    @property
    def level(self) -> int:
        return self._level

    @property
    def nickname(self) -> str:
        return self._nickname

    @property
    def name(self) -> str:
        return self._species.name

    @property
    def description(self) -> str:
        return self._species.description

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

    @property
    def is_knocked_out(self) -> bool:
        return self.current_hp == 0

    def raise_attribute(self, position: int) -> None:
        try:
            self._attribute_manager.raise_attribute(position)
        except IndexError:
            raise Exception("Tried to raise an Attribute, but it was out of bounds:", position)

    def heal(self, amount: int) -> None:
        self._current_hp += amount
        if self._current_hp > self.max_hp:
            self._current_hp = self.max_hp

    def heal_to_full(self) -> None:
        self._current_hp = self.max_hp

    def receive_damage(self, amount: int) -> None:
        self._current_hp -= amount
        if self._current_hp < 0:
            self._current_hp = 0

    @property
    def starting_mana(self) -> int:
        return self._starting_mana + self._attribute_manager.starting_mana

    @property
    def mana_per_turn(self) -> int:
        return self._mana_per_turn + self._attribute_manager.mana_per_turn

    @property
    def bench_mana_per_turn(self) -> int:
        return self._bench_mana_per_turn + self._attribute_manager.bench_mana_per_turn

    @property
    def max_mana(self) -> int:
        return self._max_mana + self._attribute_manager.max_mana

    @property
    def id(self) -> int:
        return self._id

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
    def active_abilities(self) -> List[Ability]:
        return self._ability_manager.active_abilities

    @property
    def available_abilities(self) -> List[Ability]:
        return self._ability_manager.available_abilities

    @property
    def eligible_abilities(self) -> List[Ability]:
        """
        Return available abilities that aren't already active.
        """
        return self._ability_manager.eligible_abilities

    def swap_ability(self, active_position: int, available_position: int) -> None:
        self._ability_manager.swap_ability(active_position, available_position)

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

    def add_exp(self, amount: int) -> None:
        if self._is_level_cap():
            return
        self._current_exp += amount
        self._check_level_up()

    def level_to(self, level: int) -> None:
        """
        Eg. to generate level-appropriate Elementals or test Elementals.
        """
        while self.level < level:
            self._level += 1
            self._gain_stats()
            self._increase_exp_to_level()
            self._check_raise_rank()
            self._ability_manager.check_learnable_abilities()
        self.heal_to_full()

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
            self._ability_manager.check_learnable_abilities()

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
        self._max_hp += growth_rate.max_hp + self._bonus_stat()
        self._physical_att += growth_rate.physical_att + self._bonus_stat()
        self._magic_att += growth_rate.magic_att + self._bonus_stat()
        self._physical_def += growth_rate.physical_def + self._bonus_stat()
        self._magic_def += growth_rate.magic_def + self._bonus_stat()
        self._speed += growth_rate.speed + self._bonus_stat()

    def _bonus_stat(self) -> int:
        """
        Every 20 levels, Elemental gains +1 additional of each stat.
        """
        bonus = math.floor(self._level / 20)
        return int(bonus)

    def _check_raise_rank(self) -> None:
        """
        Elementals gain a rank at level 6, 12, 18...
        TODO: Item requirements.
        """
        if self._level % 6 == 0:
            self._attribute_manager.raise_rank()
            self._ability_manager.check_learnable_abilities()

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
