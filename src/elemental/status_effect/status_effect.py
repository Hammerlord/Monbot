from enum import Enum

from src.elemental.ability.technique import Technique


class EffectType(Enum):
    BUFF = 0
    DEBUFF = 1


class StatusEffect(Technique):

    """
    A status effect applied onto a CombatElemental.
    **Most effects are temporary, so they mutate the CombatElemental's
    StatusManager rather than the CombatElemental directly.**
    Many methods are no-op by default, that should be overridden to the desired effect.
    """

    def __init__(self):
        super().__init__()
        self.__target = None  # The CombatElemental this effect is applied to.
        self.__applier = None  # The CombatElemental that applied this StatusEffect.
        self.icon = ''  # The emote that represents the effect.
        self.effect_type = EffectType.BUFF
        # Pass duration in number of the affected Elemental's turns. -1 if no duration:
        self.max_duration = self._calculate_duration(self._base_duration)
        self._duration_remaining = 0
        self.is_dispellable = True
        self.ends_on_switch = True
        self.max_stacks = 1  # Ie. can we apply multiple of this effect?
        self.current_stacks = 1
        self.can_add_instances = False  # Ie. can we apply multiple instances of this effect?
        self.bonus_multiplier = 1

    @property
    def can_stack(self) -> bool:
        return self.current_stacks < self.max_stacks

    @property
    def _base_duration(self) -> float:
        """
        :return: The number of turns this status effect lasts, in terms of your Elemental's turns.
        Examples:
        0.5 = Lasts until the start of your next turn
        2 = Lasts for two full turns
        See _calculate_duration.
        """
        return 0

    @property
    def duration_remaining(self) -> int:
        return self._duration_remaining

    @property
    def target(self):
        """
        :return: The CombatElemental this StatusEffect is applied to.
        """
        return self.__target

    @target.setter
    def target(self, combat_elemental) -> None:
        """
        :param combat_elemental: CombatElemental
        """
        self.__target = combat_elemental

    @property
    def applier(self):
        """
        :return: The CombatElemental that applied this StatusEffect.
        """
        return self.__applier

    @applier.setter
    def applier(self, elemental) -> None:
        """
        :param elemental: CombatElemental
        """
        self.__applier = elemental

    @property
    def can_reduce_duration(self) -> bool:
        return self._duration_remaining > 0

    @property
    def duration_ended(self) -> bool:
        return self._duration_remaining == 0

    def reapply(self) -> None:
        self.add_stack()
        self.refresh_duration()

    def add_stack(self) -> None:
        if self.can_stack:
            self.current_stacks += 1

    def refresh_duration(self) -> None:
        self._duration_remaining = self.max_duration

    def reduce_duration(self) -> None:
        if self.can_reduce_duration:
            self._duration_remaining -= 1

    def on_turn_start(self) -> None:
        pass

    def on_turn_end(self) -> None:
        pass

    def on_switch_in(self) -> None:
        pass

    def on_knockout(self) -> None:
        pass

    def on_receive_ability(self, ability, actor) -> None:
        """
        :param ability: The incoming Ability.
        :param actor: The CombatElemental using the Ability.
        """
        pass

    def on_receive_damage(self, amount: int, actor) -> None:
        """
        :param amount: The damage received.
        :param actor: The CombatElemental dealing the damage.
        """
        pass

    def on_damage_dealt(self) -> None:
        pass

    def on_effect_start(self) -> None:
        """
        Apply any stat changes immediately even though they are recalculated at the end of the turn.
        Eg. this allows Defend to block end-of-turn debuff damage.
        """
        self.apply_stat_changes()

    def apply_stat_changes(self) -> None:
        """
        Alter the stages on the StatusManager, if applicable.
        Call self.add_<stat>_stages to make the stat changes so that we don't have to keep constant track
        of the target structure.
        See update_p_att_stages.
        """
        pass

    def on_effect_end(self) -> None:
        pass

    def on_dispel(self, dispeller) -> None:
        """
        :param dispeller: The CombatElemental who dispelled the StatusEffect
        """
        pass

    def on_combat_start(self) -> None:
        pass

    def _update_p_att_stages(self, amount: int) -> None:
        self.target.update_p_att_stages(amount)

    def _update_m_att_stages(self, amount: int) -> None:
        self.target.update_m_att_stages(amount)

    def _update_p_def_stages(self, amount: int) -> None:
        self.target.update_p_def_stages(amount)

    def _update_m_def_stages(self, amount: int) -> None:
        self.target.update_m_def_stages(amount)

    def _update_speed_stages(self, amount: int) -> None:
        self.target.update_speed_stages(amount)

    @staticmethod
    def _calculate_duration(num_turns: float) -> int:
        """
         *2 for decrementing on enemy turn end and self turn end, so that effects can end after
         your Elemental's turn, or after your enemy's turn.
         +1 to account for the initial on_turn_end when the effect is applied, ie. so that your 1 turn duration
         effect doesn't just end immediately.
        """
        return int(num_turns * 2 + 1)
