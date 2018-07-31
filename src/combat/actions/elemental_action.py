from src.combat.actions.action import ActionType, Action, EventLog
from src.core.targetable_interface import Targetable
from src.elemental.ability.ability import TurnPriority, Ability, Target
from src.elemental.ability.damage_calculator import DamageCalculator
from src.elemental.combat_elemental import CombatElemental, CombatElementalLog


class ElementalAction(Action):
    """
    An action taken by a CombatElemental.
    """

    def __init__(self,
                 actor: CombatElemental,
                 ability: Ability,
                 combat):
        """
        :param combat: Combat
        """
        self.actor = actor
        self.ability = ability
        self.combat = combat
        self.target = None  # Determined on execution.
        self.damage_calculator = None  # Instantiated on execution.
        self.total_healing = 0  # This includes overhealing.
        self.target_effects_applied = []  # List[StatusEffect]
        self.target_effects_failed = []  # List[StatusEffect]

    def __repr__(self):
        return f"{self.recap} {self.final_damage} damage dealt."

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

    @property
    def action_type(self) -> ActionType:
        return ActionType.ELEMENTAL_ACTION

    @property
    def recap(self) -> str:
        if self.actor.is_cast_in_progress:
            recap = self.ability.get_channeling_message(self.actor.nickname)
        else:
            recap = self.ability.get_recap(self.actor.nickname)
        if self.damage_calculator.is_effective:
            recap += " It's super effective."
        elif self.damage_calculator.is_resisted:
            recap += f' The attack was resisted...'
        if self.damage_blocked > 0:
            recap += f'\n{self.target.nickname} defended the attack!'
        return recap

    @property
    def can_execute(self) -> bool:
        return (self.team.active_elemental
                and not self.team.active_elemental.is_knocked_out
                and self.team.active_elemental == self.actor)

    def execute(self) -> 'ElementalAction':
        self._setup_target()
        self.actor.on_ability(self.ability)
        self.team.log(self.ability.get_recap(self.actor.nickname))
        self.target.on_receive_ability(self.ability, self.actor)
        self._check_damage_dealt()
        self._check_actor_healing()
        self._check_target_healing()
        self._check_status_effect_application()
        self.actor.add_action(self)
        self.team.end_turn()
        return self

    def _setup_target(self) -> None:
        """
        Get the target only when we are actually executing this ability, as the enemy active elemental may have
        changed beforehand, eg. because of a switch.
        """
        self.target = self.combat.get_target(self.ability, self.actor)
        self.damage_calculator = DamageCalculator(self.target,
                                                  self.actor,
                                                  self.ability)

    def _check_damage_dealt(self) -> None:
        if self.ability.attack_power > 0:
            # Only bother with damage calculation if the Ability is meant to do damage.
            self.damage_calculator.calculate()
            damage = self.damage_calculator.final_damage
            self.target.receive_damage(damage, self.actor)
            self.team.log(self.recap)

    def _check_actor_healing(self) -> None:
        # Healing is a percentage based on the caster's maximum HP.
        assert self.ability.actor_recovery <= 1
        healing_percentage = self.ability.actor_recovery
        if healing_percentage > 0:
            healing_percentage *= self.ability.get_bonus_multiplier(self.target, self.actor)
            total_healing = healing_percentage * self.actor.max_hp
            self.actor.heal(total_healing)
            self.total_healing += int(total_healing)

    def _check_target_healing(self) -> None:
        # Healing is a percentage based on the caster's maximum HP.
        assert self.ability.target_recovery <= 1
        healing_percentage = self.ability.target_recovery
        if healing_percentage > 0:
            # Recovery abilities don't scale off of anything besides the bonus... yet
            healing_percentage *= self.ability.get_bonus_multiplier(self.target, self.actor)
            total_healing = healing_percentage * self.actor.max_hp
            self.target.heal(total_healing)
            self.total_healing += int(total_healing)

    def _check_status_effect_application(self) -> None:
        status_effect = self.ability.status_effect
        if not status_effect:
            return
        status_effect.applier = self.actor
        if self.target.add_status_effect(status_effect):
            self.target_effects_applied.append(status_effect)
        else:
            self.target_effects_failed.append(status_effect)
