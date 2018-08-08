from enum import Enum

from src.core.elements import Category
from src.core.targetable_interface import Targetable
from src.elemental.ability.technique import Technique


class EffectType(Enum):
    """
    Is it a stun, etc.
    """
    NONE = 0
    BLEED = 1
    BURN = 2
    CHILL = 3
    STUN = 4
    FREEZE = 5
    POISON = 6
    SWITCH_PREVENTION = 7
    STAT_REDUCTION = 8
    STAT_INCREASE = 9
    HEAL_OVER_TIME = 10


class StatusEffect(Technique):

    """
    A status effect applied onto a Targetable (CombatElemental or CombatTeam).
    Many methods are no-op by default, that should be overridden to the desired effect.
    """

    def __init__(self):
        super().__init__()
        self.__target = None  # The Targetable this effect is applied to.
        self.__applier = None  # The CombatElemental that applied this StatusEffect.
        self.icon = ''  # The emote that represents the effect.
        self.effect_type = EffectType.NONE
        self.category = Category.PHYSICAL
        self.turns_remaining = -1
        self.rounds_remaining = -1
        self.is_dispellable = True
        self.ends_on_switch = True
        self.max_stacks = 1  # Ie. can we apply multiple of this effect?
        self.current_stacks = 1
        self.can_add_instances = False  # Ie. can we apply multiple instances of this effect?
        self.bonus_multiplier = 1
        self.refresh_duration()
        self.active = True  # Effect may be disabled for a reason besides duration ending.

    @property
    def is_debuff(self) -> bool:
        """
        TODO there are probably buff categories
        """
        return (self.effect_type != EffectType.NONE and
                self.effect_type != EffectType.STAT_INCREASE and
                self.effect_type != EffectType.HEAL_OVER_TIME)

    def is_type(self, effect_type: EffectType) -> bool:
        return self.effect_type == effect_type

    @property
    def can_stack(self) -> bool:
        return self.current_stacks < self.max_stacks

    @property
    def turn_duration(self) -> int:
        """
        The number of turns that this effect lasts for. Decrements on turn end.
        Return -1 if this effect lasts forever/its duration is unaffected by turns.
        """
        raise NotImplementedError

    @property
    def round_duration(self) -> int:
        """
        The number of rounds that this effect lasts for. A round is when every participant's moves have been resolved.
        Most effects will use turn_duration instead. Return -1 if this effect's duration is unaffected by rounds.
        """
        return -1

    @property
    def target(self):
        """
        :return: The original CombatElemental this StatusEffect is applied to.
        """
        return self.__target

    @target.setter
    def target(self, targetable: Targetable) -> None:
        """
        :param targetable: A CombatElemental or CombatTeam.
        """
        self.__target = targetable

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
    def duration_ended(self) -> bool:
        return self.turns_remaining == 0 or self.rounds_remaining == 0

    def boost_turn_duration(self) -> None:
        """
        If the applier added this effect to itself or its own team, +1 duration to
        make up for the decrement at the end of the application turn.
        """
        assert(self.target is not None and self.applier is not None)
        if self.turns_remaining > 0:
            self.turns_remaining += 1

    def reapply(self) -> None:
        self.add_stack()
        self.refresh_duration()

    def add_stack(self) -> None:
        if self.can_stack:
            self.current_stacks += 1
            self._on_add_stack()

    def _on_add_stack(self) -> None:
        pass

    def reset_stacks(self) -> None:
        self.current_stacks = 1

    def refresh_duration(self) -> None:
        self.turns_remaining = self.turn_duration
        self.rounds_remaining = self.round_duration

    def reduce_turn_duration(self) -> None:
        if self.turns_remaining > 0:
            self.turns_remaining -= 1
            # A status effect's duration either uses turns or rounds--they're mutually exclusive.
            assert (not self.round_duration >= 0)

    def reduce_round_duration(self) -> None:
        if self.rounds_remaining > 0:
            self.rounds_remaining -= 1
            assert (not self.turn_duration >= 0)

    def on_turn_start(self) -> True:
        """
        :return True if this triggered.
        """
        pass

    def on_turn_end(self) -> True:
        """
        :return True if this triggered.
        """
        pass

    def on_round_end(self) -> True:
        """
        :return True if this triggered.
        """
        pass

    def on_switch_in(self) -> True:
        """
        :return True if this triggered.
        """
        pass

    def on_knockout(self) -> True:
        """
        :return True if this triggered.
        """
        pass

    def on_receive_ability(self, ability, actor) -> True:
        """
        :param ability: The incoming Ability.
        :param actor: The CombatElemental using the Ability.
        :return True if this triggered.
        """
        pass

    def on_receive_damage(self, amount: int, actor) -> True:
        """
        :param amount: The damage received.
        :param actor: The CombatElemental dealing the damage.
        :return True if this triggered.
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

    def on_effect_end(self) -> True:
        """
        :return True if this triggered.
        """
        pass

    def on_dispel(self, dispeller) -> True:
        """
        :param dispeller: The CombatElemental who dispelled the StatusEffect
        :return True if this triggered.
        """
        pass

    def on_combat_start(self) -> True:
        """
        :return True if this triggered.
        """
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

    @property
    def trigger_recap(self) -> str:
        # Recap message for when this effect triggers.
        return ''

    @property
    def application_recap(self) -> str:
        # Recap message for when this effect is applied.
        return ''

    @property
    def fade_recap(self) -> str:
        # Recap when this effect falls off.
        return ''
