from typing import List

from src.elemental.ability.ability import Ability
from src.elemental.status_effect.status_effect import StatusEffect


class StatusManager:
    def __init__(self, combat_elemental):
        """
        :param combat_elemental: CombatElemental
        """
        self.combat_elemental = combat_elemental
        self.num_stuns = 0  # Multiple status effects can apply a stack of this. If num > 0, then the effect is true.
        self.num_freezes = 0
        self.num_chills = 0
        self.num_blocks = 0  # How many "blocking damage" buffs there are
        self.switch_disabled = 0  # The number of "switch-preventing" debuffs
        self.p_att_stages = 0
        self.p_def_stages = 0
        self.m_att_stages = 0
        self.m_def_stages = 0
        self.speed_stages = 0
        self._mana_per_turn = 0
        self._max_stages = 6
        self._damage_reduction = 0  # Float. Percentage of damage reduced on incoming attacks.
        self._status_effects = []  # List[StatusEffect]

    @property
    def is_stunned(self) -> bool:
        return self.num_stuns > 0

    @property
    def is_frozen(self) -> bool:
        return self.num_freezes > 0

    @property
    def is_chilled(self) -> bool:
        return self.num_chills > 0

    @property
    def is_blocking(self) -> bool:
        return self.num_blocks > 0

    @property
    def can_switch(self) -> bool:
        return self.switch_disabled == 0

    @property
    def status_effects(self) -> List[StatusEffect]:
        return self._status_effects

    @property
    def num_status_effects(self) -> int:
        """
        Some attacks scale based on the number of StatusEffects a CombatElemental has.
        """
        return len(self._status_effects)

    @property
    def bonus_physical_att(self) -> int:
        return self.__calculate_stages(self.p_att_stages, self.combat_elemental.base_physical_att)

    @property
    def bonus_magic_att(self) -> int:
        return self.__calculate_stages(self.m_att_stages, self.combat_elemental.base_magic_att)

    @property
    def bonus_physical_def(self) -> int:
        return self.__calculate_stages(self.p_def_stages, self.combat_elemental.base_physical_def)

    @property
    def bonus_magic_def(self) -> int:
        return self.__calculate_stages(self.m_def_stages, self.combat_elemental.base_magic_def)

    @property
    def bonus_speed(self) -> int:
        return self.__calculate_stages(self.speed_stages, self.combat_elemental.base_speed)

    @property
    def bonus_mana_per_turn(self) -> int:
        return self._mana_per_turn

    @property
    def damage_reduction(self) -> float:
        return self._damage_reduction

    def update_p_att_stages(self, amount: int) -> None:
        self.p_att_stages = self.__validate_stages(self.p_att_stages, amount)

    def update_m_att_stages(self, amount: int) -> None:
        self.m_att_stages = self.__validate_stages(self.m_att_stages, amount)

    def update_p_def_stages(self, amount: int) -> None:
        self.p_def_stages = self.__validate_stages(self.p_def_stages, amount)

    def update_m_def_stages(self, amount: int) -> None:
        self.m_def_stages = self.__validate_stages(self.m_def_stages, amount)

    def update_speed_stages(self, amount: int) -> None:
        self.speed_stages = self.__validate_stages(self.speed_stages, amount)

    def update_mana_per_turn(self, amount: int) -> None:
        self._mana_per_turn += amount

    def update_damage_reduction(self, amount: int) -> None:
        self._damage_reduction += amount

    def __validate_stages(self, stages: int, amount: int) -> int:
        """
        A CombatElemental's stat stages are capped by a maximum number.
        :return: The capped number of stages if it exceeds the range, otherwise return the addition.
        """
        added = stages + amount
        if added > self._max_stages:
            return self._max_stages
        if added < -self._max_stages:
            return -self._max_stages
        return added

    def add_status_effect(self, status_effect: StatusEffect) -> None:
        equivalent_effect = self.__effect_exists(status_effect)
        if equivalent_effect and not status_effect.can_add_instances:
            equivalent_effect.reapply()
            return
        status_effect.target = self.combat_elemental
        self._status_effects.append(status_effect)
        status_effect.on_effect_start()
        self.__recalculate_effects()

    def dispel_all(self, dispeller) -> None:
        """
        :param dispeller: CombatElemental
        """
        for effect in self._status_effects:
            if effect.is_dispellable:
                self._status_effects.remove(effect)
                effect.on_dispel(dispeller)

    def on_receive_ability(self, ability: Ability, actor) -> None:
        """
        :param ability: The incoming Ability being received.
        :param actor: The CombatElemental performing the ability.
        """
        for effect in self._status_effects:
            effect.on_receive_ability(ability, actor)

    def on_receive_damage(self, amount, actor) -> None:
        """
        :param amount: The amount of damage received.
        :param actor: The CombatElemental dealing damage.
        """
        for effect in self._status_effects:
            effect.on_receive_damage(amount, actor)

    def on_turn_end(self) -> None:
        for effect in self._status_effects:
            effect.on_turn_end()
            if self.combat_elemental.is_knocked_out:
                return
            self.__check_effect_end(effect)
        self.__recalculate_effects()

    def on_switch_out(self) -> None:
        """
        Presently, there are no on_switch_out effects.
        """
        for effect in self._status_effects:
            if effect.ends_on_switch:
                self._status_effects.remove(effect)

    def on_switch_in(self) -> None:
        for effect in self._status_effects:
            effect.on_switch_in()

    def __effect_exists(self, status_effect: StatusEffect) -> StatusEffect or None:
        """
        Check if an equivalent StatusEffect is already on this CombatElemental by ID.
        :return The StatusEffect if it exists, None if not.
        """
        for effect in self._status_effects:
            if effect.id == status_effect.id:
                return effect

    @staticmethod
    def __calculate_stages(stages: int, stats: int) -> int:
        """
        :param stages: The number of stages a particular stat has.
        :param stats: How much of a particular stat the CombatElemental has. Eg. CombatElemental.physical_att
        :return: The amount of a stat gained or lost based on the number of stages.
        """
        if stages == 0:
            return 0
        scale = 4
        if stages > 0:
            calculation = stats * (scale + stages) // scale
        else:
            calculation = stats * scale // (scale - stages)
        return calculation - stats

    def __check_effect_end(self, effect: StatusEffect) -> None:
        effect.reduce_duration()
        if effect.duration_ended:
            self._status_effects.remove(effect)

    def __recalculate_effects(self) -> None:
        """
        Reset stat bonuses/penalties and recalculate them from changes in StatusEffects.
        Eg. when a buff or debuff falls off.
        """
        self.__reset_status()
        for effect in self._status_effects:
            effect.apply_stat_changes()

    def __reset_status(self):
        self.num_stuns = 0
        self.num_freezes = 0
        self.num_chills = 0
        self.num_blocks = 0
        self.p_att_stages = 0
        self.p_def_stages = 0
        self.m_att_stages = 0
        self.m_def_stages = 0
        self.speed_stages = 0
        self._mana_per_turn = 0
        self._damage_reduction = 0