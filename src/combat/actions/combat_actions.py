from src.combat.actions.action import Action, ActionType
from src.elemental.ability.ability import Ability, TurnPriority, Target


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
            self.old_active.on_switch_out()
            self.old_active.add_action(self)
        self.new_active.on_switch_in()
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


class UseItem(Action):
    """
    Uses an item on a target CombatElemental.
    """

    def __init__(self,
                 item,
                 elemental,
                 combat_team):
        """
        :param item: Item
        :param elemental: The CombatElemental the item is being used on.
        :param combat_team: CombatTeam
        """
        self.item = item
        self.combat_team = combat_team
        self.character = combat_team.owner  # Could be None.
        self.elemental = elemental

    @property
    def action_type(self) -> ActionType:
        return ActionType.ITEM

    @property
    def team(self):
        return self.combat_team

    def execute(self) -> None:
        self.team.log(self.recap)
        self.item.use_on(self.elemental)

    @property
    def turn_priority(self) -> TurnPriority:
        return TurnPriority.ITEM

    @property
    def speed(self) -> int:
        # Doesn't matter. Items are always used before abilities.
        return 0

    @property
    def recap(self) -> str:
        if self.character:
            return f"{self.character.nickname} gave {self.item.name} to {self.elemental.nickname}!"
        return f"{self.elemental.nickname} used {self.item.name}!"

    def can_execute(self) -> bool:
        """
        :return bool: True if the item can be used, but this should already have been checked beforehand.
        """
        return self.item.is_usable_on(self.elemental)
