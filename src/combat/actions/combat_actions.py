from src.combat.actions.action import Action, ActionType
from src.elemental.ability.ability import Ability, TurnPriority, Castable, Target


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
        # Doesn't matter. Switches are always resolved first.
        return 0

    @property
    def turn_priority(self) -> TurnPriority:
        return TurnPriority.SWITCH

    def execute(self) -> None:
        self.team.change_active_elemental(self.new_active)
        self.team.log(self.recap)
        if self.old_active:
            self.old_active.add_action(self)
        self.new_active.add_action(self)
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
