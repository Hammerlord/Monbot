from enum import Enum

from src.core.elements import Elements, Category


class Target(Enum):
    SELF = 0
    ENEMY = 1
    ENEMY_CLEAVE = 2
    ENEMY_AOE = 3
    ENEMY_TEAM = 4
    SELF_CLEAVE = 5
    SELF_AOE = 6


class Ability:
    """
    Basic information about an ability.
    """

    def __init__(self):
        self.name = None  # Str. TBD by descendants
        self.description = None  # Str. TBD by descendants
        self.id = 0  # Int. TBD by descendants
        self.element = Elements.NONE
        self.category = Category.NONE
        self.base_power = 0
        self.mana_cost = 0
        self.defend_cost = 0
        self.turn_priority = 0
        self.targeting = Target.ENEMY

    def execute(self, target: 'CombatElemental' or 'CombatTeam'):
        """
        What happens when you use this ability.
        """
        raise NotImplementedError


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
        self._ability = ability
        self._level_required = 0
        self._p_att_rank_required = 0  # Attribute ranks required, eg. Ferocity, Attunement, etc.
        self._m_att_rank_required = 0
        self._p_def_rank_required = 0
        self._hp_rank_required = 0
        self._m_def_rank_required = 0
        self._speed_rank_required = 0

    @property
    def ability_id(self) -> int:
        return self._ability.id

    @property
    def name(self) -> str:
        return self._ability.name

    @property
    def ability(self) -> Ability:
        return self._ability

    @property
    def level_required(self) -> int:
        return self._level_required

    @level_required.setter
    def level_required(self, level: int) -> None:
        self._level_required = level

    @property
    def p_att_rank_required(self) -> int:
        return self._p_att_rank_required

    @p_att_rank_required.setter
    def p_att_rank_required(self, amount: int) -> None:
        self._p_att_rank_required = amount

    @property
    def m_att_rank_required(self) -> int:
        return self._m_att_rank_required

    @m_att_rank_required.setter
    def m_att_rank_required(self, amount: int) -> None:
        self._m_att_rank_required = amount

    @property
    def p_def_rank_required(self) -> int:
        return self._p_def_rank_required

    @p_def_rank_required.setter
    def p_def_rank_required(self, amount: int) -> None:
        self._p_def_rank_required = amount

    @property
    def hp_rank_required(self) -> int:
        return self._hp_rank_required

    @hp_rank_required.setter
    def hp_rank_required(self, amount: int) -> None:
        self._hp_rank_required = amount

    @property
    def m_def_rank_required(self) -> int:
        return self._m_def_rank_required

    @m_def_rank_required.setter
    def m_def_rank_required(self, amount: int) -> None:
        self._m_def_rank_required = amount

    @property
    def speed_rank_required(self) -> int:
        return self._speed_rank_required

    @speed_rank_required.setter
    def speed_rank_required(self, amount: int) -> None:
        self._speed_rank_required = amount

    def are_requirements_fulfilled(self, elemental) -> bool:
        """
        :param elemental: The Elemental trying to learn this ability.
        """
        return \
            elemental.level >= self._level_required and \
            elemental.ferocity >= self._p_att_rank_required and \
            elemental.attunement >= self._m_att_rank_required and \
            elemental.sturdiness >= self._p_def_rank_required and \
            elemental.resolve >= self._hp_rank_required and \
            elemental.resistance >= self._m_def_rank_required and \
            elemental.swiftness >= self._speed_rank_required
