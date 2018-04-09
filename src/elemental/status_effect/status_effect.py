class StatusEffect:

    """
    A status effect applied onto an Elemental.
    Many methods are no-op by default, that should be overridden to the desired effect.
    """

    def __init__(self):
        self._id = 0
        self._name = None  # Str. TBD by descendants.
        self._description = None  # Str. TBD by descendants.
        self._target = None  # The CombatElemental this StatusEffect is applied to.
        self._applier = None  # The CombatElemental that applied this StatusEffect.
        self._max_duration = 0
        self._duration_remaining = 0  # Set to -1 if no duration.
        self.is_dispellable = True
        self.fades_on_switch = True

    @property
    def name(self) -> str:
        return self._name

    @property
    def description(self) -> str:
        return self._description

    @property
    def id(self) -> int:
        return self._id

    @property
    def max_duration(self) -> int:
        return self._max_duration

    @property
    def duration_remaining(self) -> int:
        return self._duration_remaining

    @property
    def target(self):
        """
        :return: The CombatElemental this StatusEffect is applied to.
        """
        return self._target

    @target.setter
    def target(self, elemental) -> None:
        """
        :param elemental: CombatElemental
        """
        self._target = elemental

    @property
    def applier(self):
        """
        :return: The CombatElemental that applied this StatusEffect.
        """
        return self._applier

    @applier.setter
    def applier(self, elemental) -> None:
        """
        :param elemental: CombatElemental
        """
        self._applier = elemental

    def refresh_duration(self) -> None:
        self._duration_remaining = self._max_duration

    def reduce_duration(self) -> None:
        if self.can_reduce_duration:
            self._duration_remaining -= 1

    @property
    def can_reduce_duration(self) -> bool:
        return self._duration_remaining > 0

    @property
    def duration_ended(self) -> bool:
        return self._duration_remaining == 0

    def on_turn_start(self):
        pass

    def on_turn_end(self):
        pass

    def on_switch_in(self):
        pass

    def on_switch_out(self):
        pass

    def on_knockout(self):
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

    def on_damage_dealt(self):
        pass

    def on_effect_start(self):
        pass

    def apply_stat_changes(self) -> None:
        """
        Alter the CombatElemental's main stats, if applicable.
        """
        pass

    def on_effect_end(self):
        pass

    def on_dispel(self, dispeller):
        """
        :param dispeller: The CombatElemental who dispelled the StatusEffect
        """
        pass

    def on_combat_start(self):
        pass

    def on_combat_end(self):
        pass

    def get_recap(self) -> str:
        """
        Summarize the effect in a string.
        """
        raise NotImplementedError
