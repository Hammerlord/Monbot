from typing import List

from src.elemental.ability.ability import Ability
from src.elemental.status_effect.status_effect import StatusEffect, EffectType


class StatusManager:
    def __init__(self, combat_elemental):
        """
        :param combat_elemental: CombatElemental
        """
        self.combat_elemental = combat_elemental
        self._max_stages = 6
        self._status_effects = []  # List[StatusEffect]

    @property
    def is_stunned(self) -> bool:
        return self.__has_effect(EffectType.STUN)

    @property
    def is_frozen(self) -> bool:
        return self.__has_effect(EffectType.FREEZE)

    @property
    def is_chilled(self) -> bool:
        return self.__has_effect(EffectType.CHILL)

    @property
    def is_burning(self) -> bool:
        return self.__has_effect(EffectType.BURN)

    @property
    def can_switch(self) -> bool:
        return not self.__has_effect(EffectType.SWITCH_PREVENTION)

    @property
    def is_defending(self) -> bool:
        return self.__has_effect(EffectType.DEFEND)

    @property
    def is_blocking(self) -> bool:
        return self.damage_reduction > 0

    @property
    def status_effects(self) -> List[StatusEffect]:
        return list(self._status_effects)

    @property
    def num_debuffs(self) -> int:
        return len([effect for effect in self.status_effects if effect.is_debuff])

    @property
    def num_status_effects(self) -> int:
        """
        Eg. Some attacks scale based on the number of StatusEffects a CombatElemental has.
        """
        return len(self._status_effects)

    @property
    def bonus_physical_att(self) -> int:
        stages = sum([effect.p_att_stages for effect in self.status_effects])
        return self.__calculate_stats_from_stages(self.__validate_stages(stages),
                                                  self.combat_elemental.base_physical_att)

    @property
    def bonus_magic_att(self) -> int:
        stages = sum([effect.m_att_stages for effect in self.status_effects])
        return self.__calculate_stats_from_stages(self.__validate_stages(stages),
                                                  self.combat_elemental.base_magic_att)

    @property
    def bonus_physical_def(self) -> int:
        stages = sum([effect.p_def_stages for effect in self.status_effects])
        return self.__calculate_stats_from_stages(self.__validate_stages(stages),
                                                  self.combat_elemental.base_physical_def)

    @property
    def bonus_magic_def(self) -> int:
        stages = sum([effect.m_def_stages for effect in self.status_effects])
        return self.__calculate_stats_from_stages(self.__validate_stages(stages),
                                                  self.combat_elemental.base_magic_def)

    @property
    def bonus_speed(self) -> int:
        stages = sum([effect.speed_stages for effect in self.status_effects])
        return self.__calculate_stats_from_stages(self.__validate_stages(stages),
                                                  self.combat_elemental.base_speed)

    @property
    def bonus_mana_per_turn(self) -> int:
        return sum([effect.mana_per_turn for effect in self.status_effects])

    @property
    def damage_reduction(self) -> float:
        return sum([effect.damage_reduction for effect in self.status_effects])

    def clear_status_effects(self) -> None:
        # TODO some effects may ought to linger after knockout
        self._status_effects = []

    def __validate_stages(self, stages: int) -> int:
        """
        A CombatElemental's stat stages are capped by a maximum number.
        :return: The capped number of stages if it exceeds the range.
        """
        if stages > self._max_stages:
            return self._max_stages
        if stages < -self._max_stages:
            return -self._max_stages
        return stages

    def add_status_effect(self, effect: StatusEffect) -> None:
        equivalent_effect = self.__effect_exists(effect)
        if equivalent_effect and not effect.can_add_instances:
            equivalent_effect.reapply()
        else:
            self._status_effects.append(effect)
        effect.target = self.combat_elemental
        if effect.applier == self.combat_elemental:
            effect.boost_turn_duration()
        effect.on_effect_start()

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
            if effect.on_receive_ability(ability, actor):
                self.combat_elemental.append_recent_log(effect.trigger_recap)
                self.__check_effect_end(effect)

    def on_receive_damage(self, amount, actor) -> None:
        """
        :param amount: The amount of damage received.
        :param actor: The CombatElemental dealing damage.
        """
        for effect in self._status_effects:
            if effect.on_receive_damage(amount, actor):
                self.combat_elemental.append_recent_log(effect.trigger_recap)
                self.__check_effect_end(effect)

    def on_turn_start(self) -> None:
        for effect in self._status_effects:
            if effect.on_turn_start():
                self.combat_elemental.log(effect.trigger_recap)

    def on_turn_end(self) -> None:
        for effect in self._status_effects:
            if effect.on_turn_end():
                self.combat_elemental.append_recent_log(effect.trigger_recap)
        # Only decrement and check duration end after all effects have been resolved.
        for effect in self._status_effects:
            effect.reduce_turn_duration()
            self.__check_effect_end(effect)

    def on_round_end(self) -> None:
        for effect in self._status_effects:
            if effect.on_round_end():
                self.combat_elemental.append_recent_log(effect.trigger_recap)
        # Only decrement and check duration end after all effects have been resolved.
        for effect in self._status_effects:
            effect.reduce_round_duration()
            self.__check_effect_end(effect)

    def on_opponent_changed(self, old_opponent) -> None:
        """
        :param old_opponent: CombatElemental
        """
        for effect in self._status_effects:
            if effect.ends_on_applier_changed and effect.applier == old_opponent:
                self._status_effects.remove(effect)

    def on_switch_out(self) -> None:
        """
        Presently, there are no on_switch_out effects.
        """
        for effect in self._status_effects:
            if effect.ends_on_switch:
                self._status_effects.remove(effect)

    def on_switch_in(self) -> None:
        for effect in self._status_effects:
            if effect.on_switch_in():
                self.combat_elemental.log(effect.trigger_recap)

    def __effect_exists(self, to_check: StatusEffect) -> StatusEffect or None:
        """
        Check if an equivalent StatusEffect is already on this CombatElemental by type.
        :return The StatusEffect if it exists, None if not.
        """
        return next((effect for effect in self._status_effects if type(effect) is type(to_check)), None)

    @staticmethod
    def __calculate_stats_from_stages(stages: int, stats: int) -> int:
        """
        :param stages: The number of stages a particular stat has.
        :param stats: How much of a particular stat the CombatElemental has. Eg. CombatElemental.physical_att
        :return: The amount of a stat gained or lost based on the number of stages.
        """
        if stages == 0:
            return 0
        scale = 2
        if stages > 0:
            calculation = stats * (scale + stages) // scale
        else:
            calculation = stats * scale // (scale - stages)
        return calculation - stats

    def __check_effect_end(self, effect: StatusEffect) -> None:
        if effect not in self._status_effects:
            return
        if effect.duration_ended or not effect.active:
            self._status_effects.remove(effect)
            self.combat_elemental.log(effect.fade_recap)

    def __has_effect(self, effect_type: EffectType) -> bool:
        """
        Helper function to check, eg., if the elemental is stunned.
        """
        matching = next((effect for effect in self._status_effects if effect.is_type(effect_type)), None)
        return matching is not None
