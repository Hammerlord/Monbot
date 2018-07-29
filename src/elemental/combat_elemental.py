from typing import List

from copy import deepcopy, copy

from src.core.elements import Elements
from src.core.targetable_interface import Targetable
from src.elemental.ability.ability import Ability, Castable
from src.elemental.elemental import Elemental
from src.elemental.status_effect.status_effect import StatusEffect
from src.elemental.status_effect.status_manager import StatusManager


class CombatElemental(Targetable):
    def __init__(self, elemental: Elemental,
                 team):
        """
        :param team: The CombatTeam this elemental is on.
        """
        self._elemental = elemental
        self.team = team
        self.base_physical_att = elemental.physical_att
        self.base_magic_att = elemental.magic_att
        self.base_physical_def = elemental.physical_def
        self.base_magic_def = elemental.magic_def
        self.base_speed = elemental.speed
        self.defend_potency = elemental.defend_potency
        self._current_mana = elemental.starting_mana
        self._defend_charges = elemental.defend_charges
        self._mana_per_turn = elemental.mana_per_turn
        self._bench_mana_per_turn = elemental.bench_mana_per_turn
        self._status_manager = StatusManager(self)
        self._actions = []  # List[ElementalAction]  A record of the actions taken by this CombatElemental.
        self._abilities = elemental.active_abilities
        self.casting = None  # An Ability that takes time to activate or executes over multiple turns.

    def __repr__(self) -> str:
        return self.nickname

    @property
    def nickname(self) -> str:
        return self._elemental.nickname

    @property
    def id(self) -> int:
        return self._elemental.id

    @property
    def level(self) -> int:
        return self._elemental.level

    @property
    def icon(self) -> str:
        return self._elemental.left_icon

    @property
    def element(self) -> Elements:
        return self._elemental.element

    @property
    def is_stunned(self) -> bool:
        return self._status_manager.is_stunned

    @property
    def is_frozen(self) -> bool:
        return self._status_manager.is_frozen

    @property
    def is_chilled(self) -> bool:
        return self._status_manager.is_chilled

    @property
    def is_blocking(self) -> bool:
        return self._status_manager.is_blocking

    @property
    def is_burning(self) -> bool:
        return self._status_manager.is_burning

    @property
    def num_debuffs(self) -> int:
        return self._status_manager.num_debuffs

    @property
    def current_hp(self) -> int:
        # HP is based on the Elemental's.
        return self._elemental.current_hp

    @property
    def max_hp(self) -> int:
        return self._elemental.max_hp

    @property
    def health_percent(self) -> int:
        return int((self.current_hp / self.max_hp) * 100)

    @property
    def physical_att(self) -> int:
        return self.base_physical_att + self._status_manager.bonus_physical_att

    @property
    def magic_att(self) -> int:
        return self.base_magic_att + self._status_manager.bonus_magic_att

    @property
    def physical_def(self) -> int:
        return self.base_physical_def + self._status_manager.bonus_physical_att

    @property
    def magic_def(self) -> int:
        return self.base_magic_def + self._status_manager.bonus_magic_def

    @property
    def speed(self) -> int:
        return self.base_speed + self._status_manager.bonus_speed

    @property
    def damage_reduction(self) -> float:
        return self._status_manager.damage_reduction

    @property
    def defend_charges(self) -> int:
        return self._defend_charges

    @property
    def can_defend(self) -> bool:
        return self.defend_charges > 0

    @property
    def current_mana(self) -> int:
        return self._current_mana

    @property
    def max_mana(self) -> int:
        return self._elemental.max_mana

    @property
    def can_switch(self) -> bool:
        return self._status_manager.can_switch

    @property
    def available_abilities(self) -> List[Ability]:
        """
        :return: A list of Abilities where the resource (eg. mana) requirements are met.
        """
        return [ability for ability in self._abilities if self.can_use_ability(ability)]

    @property
    def abilities(self) -> List[Ability]:
        return list(self._abilities)

    @property
    def status_effects(self) -> List[StatusEffect]:
        return list(self._status_manager.status_effects)

    @property
    def num_status_effects(self) -> int:
        return self._status_manager.num_status_effects

    @property
    def is_knocked_out(self) -> bool:
        return self._elemental.is_knocked_out

    @property
    def id(self) -> int:
        return self._elemental.id

    def is_elemental(self, other: 'CombatElemental') -> bool:
        return self.id == other.id

    def set_casting(self, casted: Castable) -> None:
        self.casting = casted

    def add_exp(self, amount: int) -> None:
        self._elemental.add_exp(amount)

    def update_p_att_stages(self, amount: int) -> None:
        self._status_manager.update_p_att_stages(amount)

    def update_m_att_stages(self, amount: int) -> None:
        self._status_manager.update_m_att_stages(amount)

    def update_p_def_stages(self, amount: int) -> None:
        self._status_manager.update_p_def_stages(amount)

    def update_m_def_stages(self, amount: int) -> None:
        self._status_manager.update_m_def_stages(amount)

    def update_speed_stages(self, amount: int) -> None:
        self._status_manager.update_speed_stages(amount)

    def update_mana_per_turn(self, amount: int) -> None:
        self._status_manager.update_mana_per_turn(amount)

    def update_damage_reduction(self, amount: int) -> None:
        self._status_manager.update_damage_reduction(amount)

    def can_use_ability(self, ability: Ability) -> bool:
        return (self.current_mana >= ability.mana_cost and
                self.defend_charges >= ability.defend_cost and
                ability in self.abilities and
                ability.is_usable_by(self))

    def gain_bench_mana(self) -> None:
        """
        All eligible bench (not dead, not active) Elementals gain mana per turn.
        """
        self.update_mana(self._bench_mana_per_turn)

    def update_mana(self, amount: int) -> None:
        self._current_mana += amount
        if self.current_mana > self._elemental.max_mana:
            self._current_mana = self._elemental.max_mana

    @property
    def last_action(self):
        previous = len(self._actions) - 1
        return self._actions[previous]

    @property
    def actions(self):
        """
        :return: List[ElementalAction]
        """
        return list(self._actions)

    def add_action(self, action) -> None:
        """
        :param action: ElementalAction
        """
        self._actions.append(action)

    def dispel_all(self, dispeller: 'CombatElemental'):
        self._status_manager.dispel_all(dispeller)

    def add_status_effect(self, status_effect: StatusEffect):
        # TODO check if we can add status effects.
        self._status_manager.add_status_effect(status_effect)

    def start_turn(self) -> None:
        if not self.is_knocked_out:
            self.update_mana(self._mana_per_turn + self._status_manager.bonus_mana_per_turn)
            self._status_manager.on_turn_start()

    def end_turn(self) -> None:
        self._status_manager.on_turn_end()

    def end_round(self) -> None:
        self._status_manager.on_round_end()

    def on_ability(self, ability: Ability) -> None:
        # Logging is handled by the ElementalAction and Casting actions.
        self.update_mana(-ability.mana_cost)
        self.update_defend_charges(-ability.defend_cost)

    def log(self, recap: str) -> None:
        self.team.log(recap)

    def append_recent_log(self, recap: str) -> None:
        self.team.append_recent_log(recap)

    def update_defend_charges(self, amount: int) -> None:
        self._defend_charges += amount

    def on_receive_ability(self, ability: Ability, actor: 'CombatElemental') -> None:
        """
        :param ability: The incoming Ability being received.
        :param actor: The CombatElemental performing the ability.
        """
        self._status_manager.on_receive_ability(ability, actor)

    def receive_damage(self, amount: int, actor: 'CombatElemental') -> None:
        """
        :param amount: The final amount of damage received.
        :param actor: The CombatElemental dealing the damage.
        """
        self._elemental.receive_damage(amount)
        # TODO differentiate ability damage source from debuff damage source
        self._status_manager.on_receive_damage(amount, actor)
        if self.is_knocked_out:
            self._status_manager.clear_status_effects()

    def heal(self, amount: int) -> None:
        self._elemental.heal(amount)
        # TODO
        self.log(f'{self.nickname} recovered health!')

    def is_enemy(self, other_team) -> bool:
        return other_team.side != self.team.side

    def snapshot(self) -> 'CombatElementalLog':
        """
        Create a limited log about itself for rendering.
        """
        return CombatElementalLog(self)


class CombatElementalLog:
    """
    Containing visible details about a CombatElemental and a few identity attrs.
    """
    def __init__(self, combat_elemental: CombatElemental):
        self.level = combat_elemental.level
        self.current_hp = combat_elemental.current_hp
        self.max_hp = combat_elemental.max_hp
        self.current_mana = combat_elemental.current_mana
        self.max_mana = combat_elemental.max_mana
        self.status_effects = combat_elemental.status_effects
        self.nickname = combat_elemental.nickname
        self.defend_charges = combat_elemental.defend_charges
        self.icon = combat_elemental.icon
        self.id = combat_elemental.id
        self.team = combat_elemental.team
        self.health_percent = combat_elemental.health_percent

    def is_enemy(self, other_team) -> bool:
        return other_team.side != self.team.side
