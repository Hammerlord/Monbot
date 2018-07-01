from typing import List

from src.core.elements import Elements
from src.elemental.ability.ability import Ability
from src.elemental.elemental import Elemental
from src.elemental.status_effect.status_effect import StatusEffect
from src.elemental.status_effect.status_manager import StatusManager


class CombatElemental:
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
    def current_hp(self) -> int:
        # HP is based on the Elemental's.
        return self._elemental.current_hp

    @property
    def max_hp(self) -> int:
        return self._elemental.max_hp

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
        return self._abilities

    @property
    def status_effects(self) -> List[StatusEffect]:
        return self._status_manager.status_effects

    @property
    def num_status_effects(self) -> int:
        return self._status_manager.num_status_effects

    @property
    def is_knocked_out(self) -> bool:
        return self._elemental.is_knocked_out

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
        return self.current_mana >= ability.mana_cost and \
               self.defend_charges >= ability.defend_cost and \
               ability.is_usable_by(self)

    def gain_bench_mana(self) -> None:
        """
        All eligible bench (not dead, not active) Elementals gain mana per turn.
        """
        self.gain_mana(self._bench_mana_per_turn)

    def gain_mana(self, amount: int) -> None:
        self._current_mana += amount
        if self.current_mana > self._elemental.max_mana:
            self._current_mana = self._elemental.max_mana

    @property
    def last_action(self):
        previous = len(self._actions) - 1
        return self._actions[previous]

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
        self.gain_mana(self._mana_per_turn + self._status_manager.bonus_mana_per_turn)

    def end_turn(self) -> None:
        self._status_manager.on_turn_end()

    def on_ability(self, ability: Ability) -> None:
        # TODO
        pass

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
        self._status_manager.on_receive_damage(amount, actor)
        if self.is_knocked_out:
            self._status_manager.clear_status_effects()

    def heal(self, amount: int) -> None:
        self._elemental.heal(amount)