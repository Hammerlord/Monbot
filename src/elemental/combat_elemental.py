from typing import List

from src.elemental.ability.ability import Ability
from src.elemental.elemental import Elemental
from src.elemental.status_effect.status_effect_manager import StatusEffectManager


class CombatElemental:
    def __init__(self, elemental: Elemental):
        self._elemental = elemental
        self._current_mana = elemental.starting_mana
        self._max_mana = elemental.max_mana
        self._mana_per_turn = elemental.mana_per_turn
        self._defend_charges = elemental.defend_charges
        self._can_switch = True
        self._is_active = False
        self._status_effects = StatusEffectManager(self)
        self._actions = []  # List[CombatAction]  A record of the actions taken by this CombatElemental.
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
    def can_switch(self, set: bool) -> None:
        self._can_switch = set

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

    def on_turn_end(self) -> None:
        pass

    def on_receive_damage(self, amount: int) -> None:
        pass

    def receive_damage(self, amount: int) -> None:
        self._elemental.receive_damage(amount)
        self.on_receive_damage(amount)

    def heal(self, amount: int) -> None:
        self._elemental.heal(amount)
