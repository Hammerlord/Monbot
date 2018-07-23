from enum import Enum

from src.core.elements import Elements, Category
from src.elemental.ability.technique import Technique
from src.elemental.status_effect.status_effect import StatusEffect


class Target(Enum):
    SELF = 0
    ENEMY = 1
    ENEMY_CLEAVE = 2
    ENEMY_AOE = 3
    ENEMY_TEAM = 4
    SELF_CLEAVE = 5
    SELF_AOE = 6
    SELF_TEAM = 7


class TurnPriority(Enum):
    FLEE = 0
    SWITCH = 1  # Switch has higher priority than all abilities.
    ITEM = 2
    DEFEND = 3  # Defend is always reliable compared to other abilities.
    HIGH = 4  # Eg. for "attack first" type abilities.
    NORMAL = 5  # Most abilities are normal turn priority.
    LOW = 6

    def __gt__(self, other) -> bool:
        if self.__class__ is other.__class__:
            return self.value > other.value
        return NotImplemented


class Channelable:
    """
    A "channeled" ability can activate repeatedly over multiple turns.
    """
    def __init__(self):
        self._turns_to_channel = self.turn_duration

    @property
    def turn_duration(self) -> int:
        raise NotImplementedError

    @property
    def has_ended(self) -> bool:
        return self._turns_to_channel == 0

    @staticmethod
    def get_channeling_message(elemental) -> str:
        return f"{elemental.name}'s attack continues!"

    def decrement_time(self):
        self._turns_to_channel -= 1


class Castable:
    """
    A wrapper class for an Ability with a charge up time.
    The cast time decrement is handled here.
    """
    def __init__(self,
                 ability: 'Ability'):
        """
        :param ability: The castable ability being used.
        :param elemental: CombatElemental using the ability.
        """
        assert(ability.base_cast_time > 0)  # It better have a cast time!
        self.ability = ability
        self.turns_to_activate = self.ability.base_cast_time

    @staticmethod
    def get_casting_message(elemental_name: str) -> str:
        raise NotImplementedError

    def is_ready(self) -> bool:
        return self.turns_to_activate == 0

    def decrement_cast_time(self):
        self.turns_to_activate -= 1

    def is_initial_use(self) -> bool:
        return self.turns_to_activate == self.ability.base_cast_time


class Ability(Technique):
    """
    Basic information about an ability.
    Perhaps weirdly, it doesn't know who owns it.
    """

    def __init__(self):
        super().__init__()
        self.mana_cost = 0
        self.defend_cost = 0
        # Who goes first in the round is determined by turn_priority.
        # Higher number = higher turn priority. If it’s equal, then we match speed stats.
        self.turn_priority = TurnPriority.NORMAL
        self.targeting = Target.ENEMY
        self.icon = ':crossed_swords:'  # Generic default icon.

    @property
    def base_cast_time(self) -> int:
        """
        Override this method if an ability takes a turn to activate.
        Also be sure to implement casting_message.
        """
        return 0

    @property
    def has_cast_time(self) -> bool:
        return self.base_cast_time > 0

    @property
    def status_effect(self) -> StatusEffect or None:
        """
        Override this operation if the ability applies a status effect.
        """
        return

    @staticmethod
    def is_usable_by(combat_elemental) -> bool:
        """
        A custom use requirement (not including mana costs).
        :param combat_elemental: CombatElemental
        """
        return True

    def get_recap(self, elemental_name: str) -> str:
        return f"{elemental_name} used {self.name}!"

    @staticmethod
    def casting_message(elemental_name: str) -> str:
        return ''


class LearnableAbility:
    """
    Wraps an Ability with requirements, learnable by a particular Elemental.
    The requirements can be one or more of the following:
    elemental.level -- up to 60
    elemental.ferocity -- up to 3
    elemental.attunement -- same as ferocity, and so on
    elemental.sturdiness
    elemental.resolve
    elemental.resistance
    elemental.swiftness
    """

    def __init__(self,
                 ability: Ability,
                 level_required=0):
        self.ability = ability
        self.level_required = level_required
        self.p_att_rank_required = 0  # Attribute ranks required, eg. Ferocity, Attunement, etc.
        self.m_att_rank_required = 0
        self.p_def_rank_required = 0
        self.hp_rank_required = 0
        self.m_def_rank_required = 0
        self.speed_rank_required = 0

    @property
    def name(self) -> str:
        return self.ability.name

    @property
    def description(self) -> str:
        return self.ability.description

    @property
    def category(self) -> Category:
        return self.ability.category

    @property
    def mana_cost(self) -> int:
        return self.ability.mana_cost

    @property
    def element(self) -> Elements:
        return self.ability.element

    @property
    def base_power(self) -> int:
        return self.ability.base_power

    @property
    def icon(self) -> str:
        return self.ability.icon

    def are_requirements_fulfilled(self, elemental) -> bool:
        """
        :param elemental: The Elemental trying to learn this ability.
        """
        return (elemental.level >= self.level_required and
                elemental.ferocity >= self.p_att_rank_required and
                elemental.attunement >= self.m_att_rank_required and
                elemental.sturdiness >= self.p_def_rank_required and
                elemental.resolve >= self.hp_rank_required and
                elemental.resistance >= self.m_def_rank_required and
                elemental.swiftness >= self.speed_rank_required)
