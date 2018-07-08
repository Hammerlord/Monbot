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
    LOW = 0
    NORMAL = 1  # Most abilities are normal turn priority.
    HIGH = 2  # Eg. for "attack first" type abilities.
    ITEM = 3
    SWITCH = 4  # Switch has higher priority than all abilities.
    FLEE = 5

    def __gt__(self, other) -> bool:
        if self.__class__ is other.__class__:
            return self.value > other.value
        return NotImplemented


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
