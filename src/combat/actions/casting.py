from src.combat.actions.action import Action, ActionType
from src.core.targetable_interface import Targetable
from src.elemental.ability.ability import Castable, TurnPriority
from src.elemental.combat_elemental import CombatElemental


class Casting(Action):
    """
    When a CombatElemental uses an ability with base_cast_time > 0, this Action is created instead
    of a normal ElementalAction.
    """
    def __init__(self,
                 actor: CombatElemental,
                 castable: Castable,
                 target: Targetable):
        assert (castable.ability.base_cast_time > 0)
        self.actor = actor
        self.castable = castable
        self.target = target
        self.ability = self.castable.ability

    @property
    def can_execute(self) -> bool:
        return not self.actor.is_knocked_out

    @property
    def team(self):
        return self.actor.team

    @property
    def speed(self) -> int:
        return self.actor.speed

    @property
    def turn_priority(self) -> TurnPriority:
        return self.ability.turn_priority

    def execute(self) -> None:
        if self.castable.is_initial_use():
            # Only consume mana, etc. if this was the turn the cast was started. Although I don't imagine
            # cast times will ever exceed 1 turn.
            self.actor.on_ability(self.castable.ability)
            self.actor.log(self.recap)
        self.actor.set_casting(self.castable)
        self.actor.add_action(self)
        self.castable.decrement_cast_time()
        self.team.end_turn()

    @property
    def recap(self) -> str:
        return self.ability.get_casting_message(self.actor.nickname)

    @property
    def action_type(self) -> ActionType:
        return ActionType.ELEMENTAL_ACTION
