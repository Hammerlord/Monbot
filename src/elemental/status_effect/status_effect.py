class StatusEffect:

    """
    A status effect applied onto an Elemental.
    Many methods are no-op by default, that should be overridden to the desired effect.
    """

    def __init__(self):
        self.id = 0
        self.name = None  # Str. TBD by descendants.
        self.description = None  # Str. TBD by descendants.
        self.target = None  # The CombatElemental this StatusEffect is attached to
        self.applier = None  # The CombatElemental that applied this StatusEffect
        self.max_duration = 0
        self.duration_remaining = 0  # Set to -1 if no duration.
        self.is_dispellable = True
        self.fades_on_switch = True

    def set_target(self, elemental):
        """
        :param elemental: CombatElemental
        """
        self.target = elemental

    def set_applier(self, elemental):
        """
        :param elemental: CombatElemental
        """
        self.applier = elemental

    def reduce_duration(self):
        if self.can_reduce_duration:
            self.duration_remaining -= 1

    @property
    def can_reduce_duration(self) -> bool:
        return self.duration_remaining > 0

    @property
    def duration_ended(self) -> bool:
        return self.duration_remaining == 0

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

    def on_receive_ability(self, ability: 'Ability', actor: 'CombatElemental'):
        pass

    def on_receive_damage(self, amount: int, actor: 'CombatElemental'):
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