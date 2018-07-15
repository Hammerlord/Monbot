from enum import Enum

from src.elemental.ability.ability import Ability, TurnPriority
from src.elemental.ability.damage_calculator import DamageCalculator
from src.elemental.combat_elemental import CombatElemental


class ActionType(Enum):
    NONE = 0
    ELEMENTAL_ACTION = 1
    SWITCH = 2
    KNOCKED_OUT = 3
    ITEM = 4


class StatusEffectRecap:
    @property
    def recap(self) -> str:
        raise NotImplementedError


class Action:
    @property
    def action_type(self) -> int:
        raise NotImplementedError

    @property
    def turn_priority(self) -> TurnPriority:
        raise NotImplementedError

    @property
    def team(self):
        """
        :return: CombatTeam: To identify the "owner" of this action.
        """
        raise NotImplementedError

    @property
    def speed(self) -> int:
        raise NotImplementedError

    def execute(self) -> None:
        """
        :return: bool: True if the action was successfully executed.
        """
        raise NotImplementedError

    @property
    def recap(self) -> str:
        """
        :return: Summarize the main part of the action.
        """
        raise NotImplementedError

    @property
    def can_execute(self) -> bool:
        raise NotImplementedError


class ElementalAction(Action):
    """
    An action taken by a CombatElemental.
    """

    def __init__(self,
                 actor: CombatElemental,
                 ability: Ability,
                 target: CombatElemental):
        self.actor = actor
        self.ability = ability
        self.ability_triggered_bonus = False
        self.target = target
        self.damage_calculator = DamageCalculator(self.target,
                                                  self.actor,
                                                  self.ability)
        self.target_effects_applied = []  # List[StatusEffect]
        self.target_effects_failed = []  # List[StatusEffect]
        self.actor_effects_applied = []  # List[StatusEffect]

    @property
    def team(self):
        return self.actor.team

    @property
    def turn_priority(self) -> TurnPriority:
        return self.ability.turn_priority

    @property
    def speed(self) -> int:
        return self.actor.speed

    @property
    def final_damage(self) -> int:
        return self.damage_calculator.final_damage

    @property
    def damage_blocked(self) -> int:
        return self.damage_calculator.damage_blocked

    @property
    def damage_defended(self) -> int:
        return self.damage_calculator.damage_defended

    @property
    def is_effective(self) -> bool:
        return self.damage_calculator.is_effective

    @property
    def is_resisted(self) -> bool:
        return self.damage_calculator.is_resisted

    def execute(self) -> None:
        self.actor.on_ability(self.ability)
        self.target.on_receive_ability(self.ability, self.actor)
        self.check_damage_dealt()
        self.check_healing_done()
        self.check_status_effect_application()
        self.actor.add_action(self)
        self.team.end_turn()

    def check_damage_dealt(self) -> None:
        if self.ability.base_power > 0:
            # Only run calculate() and deal damage if the Ability is meant to do damage.
            self.damage_calculator.calculate()
            damage = self.damage_calculator.final_damage
            self.target.receive_damage(damage, self.actor)

    def check_healing_done(self) -> None:
        healing = self.ability.base_recovery
        if healing > 0:
            # Recovery abilities don't scale off of anything besides the bonus... yet
            healing *= self.ability.get_bonus_multiplier(self.target, self.actor)
            self.target.heal(healing)

    def check_status_effect_application(self) -> None:
        status_effect = self.ability.status_effect
        if status_effect:
            status_effect.applier = self.actor
            if self.target.add_status_effect(status_effect):
                self.target_effects_applied.append(status_effect)
            else:
                self.target_effects_failed.append(status_effect)

    @property
    def action_type(self) -> ActionType:
        return ActionType.ELEMENTAL_ACTION

    @property
    def recap(self) -> str:
        return f"{self.actor.nickname} used {self.ability.name}!"

    @property
    def can_execute(self) -> bool:
        return self.team.active_elemental and not self.team.active_elemental.is_knocked_out


class Switch(Action):
    """
    Records the Elementals involved in a switch.
    """

    def __init__(self,
                 team,
                 old_active,
                 new_active):
        """
        :param team: CombatTeam
        :param old_active: CombatElemental or None
        :param new_active: CombatElemental
        """
        self._team = team
        self.character = team.owner
        self.old_active = old_active
        self.new_active = new_active

    @property
    def action_type(self) -> ActionType:
        return ActionType.SWITCH

    @property
    def team(self):
        return self._team

    @property
    def speed(self) -> int:
        if self.old_active:
            return self.old_active.speed
        return 0

    @property
    def turn_priority(self) -> TurnPriority:
        return TurnPriority.SWITCH

    def execute(self) -> None:
        self.team.change_active_elemental(self.new_active)
        self.team.end_turn()

    @property
    def recap(self) -> str:
        # If the team has an owner, report the Switch differently.
        if self.character:
            return self.recap_team_switch()
        return self.recap_wild_elemental_switch()

    def recap_wild_elemental_switch(self) -> str:
        new_elemental = self.new_active.nickname
        if not self.old_active or self.old_active.is_knocked_out:
            return f"{new_elemental} appeared!"
        previous_elemental = self.old_active.nickname
        return f"{previous_elemental} retreated, and {new_elemental} appeared!"

    def recap_team_switch(self) -> str:
        character_name = self.character.nickname
        new_elemental = self.new_active.nickname
        if not self.old_active or self.old_active.is_knocked_out:
            return f"{character_name} sent out {new_elemental}!"
        previous_elemental = self.old_active.nickname
        return f"{character_name} recalled {previous_elemental} and sent out {new_elemental}!"

    def can_execute(self) -> bool:
        """
        :return bool: True if we don't have an active elemental, but false if it is dead.
        """
        return not self.team.active_elemental or self.team.active_elemental.is_knocked_out


class KnockedOut(Action):
    def __init__(self,
                 combat_elemental):
        self.combat_elemental = combat_elemental

    @property
    def team(self):
        return self.combat_elemental.team

    @property
    def turn_priority(self) -> TurnPriority:
        # This "action" is for record purposes: its turn priority doesn't get checked.
        return TurnPriority.LOW

    @property
    def speed(self) -> int:
        # Same as turn_priority, this doesn't matter.
        return 0

    @property
    def action_type(self) -> ActionType:
        return ActionType.KNOCKED_OUT

    def execute(self) -> None:
        # No real operation.
        pass

    @property
    def recap(self) -> str:
        return f"{self.combat_elemental.nickname} has been knocked out!"

    @property
    def can_execute(self) -> bool:
        """
        :return bool: True if the team's combat elemental is dead.
        """
        return self.team.active_elemental.is_knocked_out
