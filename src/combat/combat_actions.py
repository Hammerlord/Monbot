from src.elemental.ability.ability import Ability
from src.elemental.ability.damage_calculator import DamageCalculator
from src.elemental.combat_elemental import CombatElemental
from src.team.combat_team import CombatTeam


class ActionType:
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

    def execute(self) -> None:
        raise NotImplementedError

    @property
    def recap(self) -> str:
        """
        :return: Summarize the main part of the action.
        """
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
        self.target_effects_applied = []
        self.target_effects_failed = []
        self.actor_effects_applied = []

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
            if self.target.add_status_effect(status_effect):
                self.target_effects_applied.append(status_effect)
            else:
                self.target_effects_failed.append(status_effect)

    @property
    def action_type(self) -> int:
        return ActionType.ELEMENTAL_ACTION

    @property
    def recap(self) -> str:
        return f"{self.actor.nickname} used {self.ability.name}!"


class Switch(Action):
    """
    Records the Elementals involved in a switch.
    """

    def __init__(self,
                 team: CombatTeam,
                 old_active: CombatElemental or None,
                 new_active: CombatElemental):
        self.team = team
        self.character = team.owner
        self.old_active = old_active
        self.new_active = new_active

    @property
    def action_type(self) -> int:
        return ActionType.SWITCH

    def execute(self) -> None:
        self.team.change_active_elemental(self.new_active)

    @property
    def recap(self) -> str:
        character_name = self.character.nickname
        previous_elemental = self.old_active.nickname
        new_elemental = self.new_active.nickname
        if not self.old_active or self.old_active.is_knocked_out:
            return f"{character_name} sent out {new_elemental}!"
        return f"{character_name} recalled {previous_elemental} and sent out {new_elemental}!"


class KnockedOut(Action):
    def __init__(self,
                 combat_elemental):
        self.combat_elemental = combat_elemental

    @property
    def action_type(self) -> int:
        return ActionType.KNOCKED_OUT

    def execute(self) -> None:
        """
        Do nothing.
        """
        pass

    @property
    def recap(self) -> str:
        return f"{self.combat_elemental.nickname} has been knocked out!"
