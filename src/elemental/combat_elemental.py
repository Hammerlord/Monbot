from typing import List

from copy import deepcopy, copy

from src.core.elements import Elements
from src.core.targetable_interface import Targetable
from src.elemental.ability.abilities.wait import Wait
from src.elemental.ability.abilities.defend import Defend
from src.elemental.ability.ability import Ability
from src.elemental.ability.queueable import Castable, Channelable, Queueable
from src.elemental.elemental import Elemental
from src.elemental.species.species import Loot
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
        self._base_damage = elemental.base_damage
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
        self._abilities.append(Defend())  # All elementals know Defend.
        # Queueable; wrapper for an Ability that takes time to activate or executes over multiple turns:
        self.action_queued = None

    def __repr__(self) -> str:
        return self.nickname

    @property
    def nickname(self) -> str:
        return self._elemental.nickname

    @property
    def id(self) -> str:
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
    def can_act(self) -> bool:
        return not self.is_stunned and not self.is_frozen and not self.is_knocked_out

    @property
    def is_chilled(self) -> bool:
        return self._status_manager.is_chilled

    @property
    def is_defending(self) -> bool:
        return self._status_manager.is_defending

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
    def base_damage(self) -> int:
        return self._base_damage

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
    def loot(self) -> List[Loot]:
        return self._elemental.loot

    @property
    def available_abilities(self) -> List[Ability]:
        """
        :return: A list of Abilities where the resource (eg. mana) requirements are met.
        """
        usable_abilities = [ability for ability in self._abilities if self.can_use_ability(ability)]
        if usable_abilities:
            return usable_abilities
        return [Wait()]

    @property
    def abilities(self) -> List[Ability]:
        return self._abilities

    @property
    def status_effects(self) -> List[StatusEffect]:
        return self._status_manager.status_effects

    @property
    def team_status_effects(self):
        return self.team.status_effects

    @property
    def num_status_effects(self) -> int:
        return self._status_manager.num_status_effects

    @property
    def is_knocked_out(self) -> bool:
        return self._elemental.is_knocked_out

    def is_elemental(self, other: 'CombatElemental') -> bool:
        return self.id == other.id

    def set_channeling(self, ability: Ability) -> None:
        if not self.action_queued:
            self.set_acting(Channelable(ability))

    def set_acting(self, acting: Queueable) -> None:
        """
        :param acting: What this CombatElemental is in the middle of performing.
        Eg. it is casting a spell with a cast time, or using an attack that triggers repeatedly across turns.
        """
        self.action_queued = acting

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

    def add_status_effect(self, effect: StatusEffect):
        # TODO check if we can add status effects.
        self._status_manager.add_status_effect(effect)
        self.continue_recent_log(effect.application_recap)

    def start_turn(self) -> None:
        if not self.is_knocked_out:
            self.update_mana(self._mana_per_turn + self._status_manager.bonus_mana_per_turn)
            self._status_manager.on_turn_start()

    def end_turn(self) -> None:
        if self.is_knocked_out:
            return
        if self.action_queued:
            self.action_queued.decrement_time()
            if self.action_queued.has_ended:
                self.action_queued = None
        self._status_manager.on_turn_end()

    def end_round(self) -> None:
        if not self.is_knocked_out:
            self._status_manager.on_round_end()

    def on_ability(self, ability: Ability) -> None:
        # Logging is handled by the ElementalAction and Casting actions.
        if self.is_cast_in_progress:
            # Then mana consumption was already handled on cast/channel start.
            return
        self.update_mana(-ability.mana_cost)
        self.update_defend_charges(-ability.defend_cost)

    def on_opponent_changed(self, opponent: 'CombatElemental') -> None:
        self._status_manager.on_opponent_changed(opponent)

    def on_switch_out(self) -> None:
        self._status_manager.on_switch_out()

    def on_switch_in(self) -> None:
        self._status_manager.on_switch_in()

    @property
    def is_cast_in_progress(self) -> bool:
        if self.action_queued:
            return not self.action_queued.is_initial_use
        return False

    def log(self, recap: str) -> None:
        self.team.log(recap)

    def append_recent_log(self, recap: str) -> None:
        self.team.append_recent_log(recap)

    def continue_recent_log(self, recap: str) -> None:
        self.team.continue_recent_log(recap)

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
            self.cancel_casting()

    def cancel_casting(self) -> None:
        self.action_queued = None

    def heal(self, amount: float) -> None:
        # TODO block ability healing when knocked out.
        if self.current_hp == self.max_hp:
            return
        self._elemental.heal(amount)
        self.log(f'{self.nickname} recovered health!')

    def is_enemy(self, other_team) -> bool:
        return other_team.side != self.team.side

    def snapshot(self) -> 'CombatElementalLog':
        """
        Create a limited log about itself for rendering.
        """
        return CombatElementalLog(self)

    @property
    def team_status(self) -> List[bool]:
        """
        A list of which elementals have or have not been knocked out on the team, as booleans.
        """
        return [not elemental.is_knocked_out for elemental in self.team.elementals]


class CombatElementalLog:
    """
    Containing visible details about a CombatElemental for rendering.
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
        self.health_percent = combat_elemental.health_percent
        self.team_status_effects = combat_elemental.team_status_effects
        self.is_knocked_out = combat_elemental.is_knocked_out
        self.action_queued = combat_elemental.action_queued
        self.team_status = combat_elemental.team_status
