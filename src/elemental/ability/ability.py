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


class TurnPriority(Enum):
    NORMAL = 1  # Most abilities are normal turn priority.
    HIGH = 2  # Eg. for "attack first" type abilities.
    SWITCH = 3  # Switch has the highest priority.


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
        self.bonus_multiplier = 1

    @property
    def status_effect(self) -> StatusEffect or None:
        """
        Override this operation if the ability applies a status effect.
        """
        return

    @staticmethod
    def is_usable_by(combat_elemental) -> bool:
        """
        A custom use requirement.
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
                 ability: Ability):
        self.ability = ability
        self.level_required = 0
        self.p_att_rank_required = 0  # Attribute ranks required, eg. Ferocity, Attunement, etc.
        self.m_att_rank_required = 0
        self.p_def_rank_required = 0
        self.hp_rank_required = 0
        self.m_def_rank_required = 0
        self.speed_rank_required = 0

    @property
    def ability_id(self) -> int:
        return self.ability.id

    @property
    def name(self) -> str:
        return self.ability.name

    def are_requirements_fulfilled(self, elemental) -> bool:
        """
        :param elemental: The Elemental trying to learn this ability.
        """
        return \
            elemental.level >= self.level_required and \
            elemental.ferocity >= self.p_att_rank_required and \
            elemental.attunement >= self.m_att_rank_required and \
            elemental.sturdiness >= self.p_def_rank_required and \
            elemental.resolve >= self.hp_rank_required and \
            elemental.resistance >= self.m_def_rank_required and \
            elemental.swiftness >= self.speed_rank_required
