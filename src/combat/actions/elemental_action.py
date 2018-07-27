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
                 target: Targetable):
        self.actor = actor
        self.ability = ability
        self.ability_triggered_bonus = False
        self.target = target
        self.damage_calculator = DamageCalculator(self.target,
                                                  self.actor,
                                                  self.ability)
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

    def execute(self) -> 'ElementalAction':
        self.on_ability()
        self.team.log(self.ability.get_recap(self.actor.nickname))
        self.target.on_receive_ability(self.ability, self.actor)
        self.check_damage_dealt()
        self.check_healing_done()
        self.check_status_effect_application()
        self.actor.add_action(self)
        self.team.end_turn()
        return self

    def on_ability(self):
        if not self.ability.has_cast_time:
            # Then mana consumption was already handled on cast start.
            self.actor.on_ability(self.ability)

    def check_damage_dealt(self) -> None:
        if self.ability.attack_power > 0:
            # Only bother with damage calculation if the Ability is meant to do damage.
            self.damage_calculator.calculate()
            damage = self.damage_calculator.final_damage
            self.target.receive_damage(damage, self.actor)
            # Log here for ability
            self.team.log(self.recap)

    def check_healing_done(self) -> None:
        # Healing is a percentage based on the caster's maximum HP.
        assert self.ability.recovery <= 1
        healing_percentage = self.ability.recovery
        if healing_percentage > 0:
            # Recovery abilities don't scale off of anything besides the bonus... yet
            healing_percentage *= self.ability.get_bonus_multiplier(self.target, self.actor)
            total_healing = healing_percentage*self.actor.max_hp
            self.target.heal(total_healing)
            self.total_healing = total_healing

    def check_status_effect_application(self) -> None:
        status_effect = self.ability.status_effect
        if not status_effect:
            return
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
                and not self.team.active_elemental.is_knocked_out)