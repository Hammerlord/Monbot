from src.elemental.ability.ability import Ability, AbilityType
from src.elemental.ability.damage_calculator import DamageCalculator
from src.elemental.combat_elemental import CombatElemental


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

    @property
    def recap(self) -> str:
        raise NotImplementedError


class ElementalAction(Action):
    """
    An action taken by a CombatElemental.
    """

    def __init__(self,
                 character,
                 actor: CombatElemental,
                 ability: Ability,
                 target: CombatElemental):
        self.character = character
        self.actor = actor
        self.ability = ability
        self.target = target
        self.damage_calculator = DamageCalculator(self.target,
                                                  self.actor,
                                                  self.ability)

    def execute(self) -> None:
        self.actor.on_ability(self.ability)
        self.target.on_receive_ability(self.ability, self.actor)
        self.check_damage_dealt()

    def check_damage_dealt(self):
        if self.ability.type == AbilityType.DAMAGE:
            # Only run calculate() and deal damage if the Ability is meant to do damage.
            self.damage_calculator.calculate()


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
                 character,
                 old_active: CombatElemental or None,
                 new_active: CombatElemental):
        self.character = character
        self.old_active = old_active
        self.new_active = new_active

    @property
    def action_type(self) -> int:
        return ActionType.SWITCH

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

    @property
    def recap(self) -> str:
        return f"{self.combat_elemental.nickname} has been knocked out!"
