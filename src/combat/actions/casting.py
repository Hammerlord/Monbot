from src.combat.actions.action import Action, ActionType
from src.core.targetable_interface import Targetable
from src.elemental.ability.ability import TurnPriority
from src.elemental.ability.queueable import Castable
from src.elemental.combat_elemental import CombatElemental


class Casting(Action):
    """
    When a CombatElemental uses an ability with base_cast_time > 0, this Action is created instead
    of a normal ElementalAction.
    """

    def __init__(self,
                 actor: CombatElemental,
                 castable: Castable):
        assert (castable.ability.base_cast_time > 0)
        self.actor = actor
        self.castable = castable
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
        if not self.actor.action_queued:
            self.actor.on_ability(self.castable.ability)
            self.actor.set_acting(self.castable)
        self.actor.log(self.recap)
        self.actor.add_action(self)
        self.team.end_turn()

    @property
    def recap(self) -> str:
        return self.ability.get_casting_message(self.actor.nickname)

    @property
    def action_type(self) -> ActionType:
        return ActionType.ELEMENTAL_ACTION
