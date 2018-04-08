from typing import List

from src.elemental.ability.ability import Ability
from src.elemental.elemental import Elemental
from src.elemental.status_effect.status_effect import StatusEffect


class CombatElemental:
    def __init__(self, elemental: Elemental):
        self._elemental = elemental
        self._current_mana = elemental.starting_mana
        self._max_mana = elemental.max_mana
        self._mana_per_turn = elemental.mana_per_turn
        self._defend_charges = elemental.defend_charges
        self._can_switch = True
        self._is_active = False
        self._physical_att = self._elemental.physical_att
        self._magic_att = self._elemental.magic_att
        self._physical_def = self._elemental.physical_def
        self._magic_def = self._elemental.magic_def
        self._speed = self._elemental.speed
        self._defend_potency = self._elemental.defend_potency
        self._status_effects = []  # List[StatusEffect]
        self._actions = []  # List[ActionLog]  A record of the actions taken by this CombatElemental.
        self._abilities = elemental.active_abilities

    @property
    def id(self) -> int:
        return self._elemental.id

    @property
    def current_hp(self) -> int:
        # HP is based on the Elemental's.
        return self._elemental.current_hp

    @property
    def max_hp(self) -> int:
        return self._elemental.max_hp

    @property
    def physical_att(self) -> int:
        return self._physical_att

    @property
    def magic_att(self) -> int:
        return self._magic_att

    @property
    def physical_def(self) -> int:
        return self._physical_def

    @property
    def magic_def(self) -> int:
        return self._magic_def

    @property
    def speed(self) -> int:
        return self._speed

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
        return self._can_switch

    @can_switch.setter
    def can_switch(self, set_switchable: bool) -> None:
        self._can_switch = set_switchable

    @property
    def abilities(self) -> List[Ability]:
        return self._abilities

    @property
    def is_knocked_out(self) -> bool:
        return self._elemental.current_hp == 0

    def on_turn_start(self) -> None:
        self.gain_mana(self._mana_per_turn)

    def gain_mana(self, amount: int) -> None:
        self._current_mana += amount
        if self.current_mana > self._max_mana:
            self._current_mana = self._max_mana

    @property
    def last_action(self):
        previous = len(self._actions) - 1
        return self._actions[previous]

    def on_ability(self) -> None:
        # TODO
        pass

    def add_status_effect(self, status_effect: StatusEffect):
        status_effect.target(self)
        self._status_effects.append(status_effect)
        status_effect.on_effect_start()

    def on_turn_end(self) -> None:
        for effect in self._status_effects:
            effect.on_turn_end()
            self._check_effect_end(effect)
        self.recalculate_effect_stats()

    def _check_effect_end(self, effect: StatusEffect) -> None:
        effect.reduce_duration()
        if effect.duration_ended:
            self._status_effects.remove(effect)

    def on_receive_ability(self, ability: Ability, actor: 'CombatElemental') -> None:
        """
        :param ability: The incoming Ability being received.
        :param actor: The CombatElemental performing the ability.
        """
        for effect in self._status_effects:
            effect.on_receive_ability(ability, actor)

    def receive_damage(self, amount: int, actor: 'CombatElemental') -> None:
        """
        :param amount: The final amount of damage received.
        :param actor: The CombatElemental dealing the damage.
        """
        self._elemental.receive_damage(amount)
        for effect in self._status_effects:
            effect.on_receive_damage(amount, actor)

    def heal(self, amount: int) -> None:
        self._elemental.heal(amount)

    def recalculate_effect_stats(self):
        """
        Recalculate stat bonuses/penalties from effects, due to changes in status effects on a per-turn basis.
        """
        self._reset_stats()
        for effect in self._status_effects:
            effect.apply_stat_changes()

    def _reset_stats(self) -> None:
        """
        Resets the CombatElemental's main stats to the referenced Elemental's stats.
        Used when recalculating stat changes from StatusEffects.
        """
        self._physical_att = self._elemental.physical_att
        self._magic_att = self._elemental.magic_att
        self._physical_def = self._elemental.physical_def
        self._magic_def = self._elemental.magic_def
        self._speed = self._elemental.speed
        self._mana_per_turn = self._elemental.mana_per_turn
        self._defend_potency = self._elemental.defend_potency