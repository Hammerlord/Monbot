from typing import List

from src.elemental.ability.ability import Ability
from src.elemental.combat_elemental import CombatElemental
from src.team.team import Team


class ElementalAction:
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

    def execute(self) -> None:
        self.actor.on_ability()
        self.target.on_receive_ability(self.ability, self.actor)
        self.ability.execute(self.target)

    @property
    def recap(self) -> str:
        return f"{self.actor.nickname} used {self.ability.name}!"


class Switch:
    """
    Records the Elementals involved in a switch.
    """
    def __init__(self,
                 character,
                 old_active: CombatElemental,
                 new_active: CombatElemental):
        self.character = character
        self.old_active = old_active
        self.new_active = new_active

    @property
    def recap(self) -> str:
        character_name = self.character.nickname
        previous_elemental = self.old_active.nickname
        new_elemental = self.new_active.nickname
        if not self.old_active.is_knocked_out:
            return f"{character_name} recalled {previous_elemental} and sent out {new_elemental}!"
        return f"{character_name} sent out {new_elemental}!"


class KnockedOut:
    def __init__(self,
                 combat_elemental):
        self.combat_elemental = combat_elemental

    @property
    def recap(self) -> str:
        return f"{self.combat_elemental.nickname} has been knocked out!"


class CombatTeam:

    """
    Wrapper class for a Team in battle. Generates CombatElemental instances of the Team's Elementals.
    The player controls the CombatTeam to manipulate Combat.
    TODO entering combat should fail if all Elementals have been knocked out.
    """

    def __init__(self,
                 team: Team):
        """
        :param team: The non-combat Team.
        """
        self.combat = None
        self.team = [CombatElemental(elemental) for elemental in team.elementals]
        self.owner = team.owner
        self._active = self.set_next_active()
        self.status_effects = []  # Team-wide status effects, eg. weather.
        self.actions = []  # list[CombatAction] taken by this team.

    def set_combat(self, combat):
        """
        :param combat: The battle this Team is joining.
        :return:
        """
        self.combat = combat
        self.combat.join_battle(self)

    @property
    def active(self) -> CombatElemental:
        return self._active

    @property
    def bench(self) -> List[CombatElemental]:
        """
        Returns the team CombatElementals minus the active one.
        """
        return [elemental for elemental in self.team if elemental != self._active]

    @property
    def can_switch(self) -> bool:
        return len(self.eligible_bench) > 0

    @property
    def eligible_bench(self) -> List[CombatElemental]:
        """
        Returns the benched CombatElementals that aren't knocked out (ie. have more than 0 HP).
        """
        return [elemental for elemental in self.team if elemental != self._active and not elemental.is_knocked_out]

    @property
    def is_npc(self) -> bool:
        return self.owner.is_npc

    @property
    def is_all_knocked_out(self) -> bool:
        """
        :return: If all Elementals on the Team have been knocked out (0 HP).
        Game over if true.
        """
        return all(elemental.is_knocked_out for elemental in self.team)

    def use_ability(self, ability: Ability) -> None:
        if self.active.is_knocked_out:
            self.actions.append(KnockedOut(self._active))
            return
        self.make_action(ability)
        self.active.on_turn_end()
        self.combat.check_end()

    def make_action(self, ability: Ability) -> None:
        action = ElementalAction(
            character=self.owner,
            actor=self.active,
            ability=ability,
            target=self.combat.get_target(ability, self.active)
        )
        action.execute()
        self.actions.append(action)

    def on_turn_start(self) -> None:
        self.active.on_turn_start()
        for elemental in self.eligible_bench:
            elemental.gain_bench_mana()

    def set_next_active(self) -> CombatElemental:
        """
        The next Elemental eligible to be active (HP > 0), meaning it is sent to the battlefield.
        """
        return next((elemental for elemental in self.team if not elemental.is_knocked_out), None)

    def switch(self, slot: int) -> None:
        """
        Switch the active Elemental with an Elemental on CombatTeam.eligible.
        """
        eligible_elementals = self.eligible_bench
        valid_slot = 0 <= slot < len(eligible_elementals) - 1  # Valid slot?
        if not valid_slot:
            return
        self.actions.append(Switch(
            character=self.owner,
            old_active=self._active,
            new_active=eligible_elementals[slot]
        ))
        self._active = eligible_elementals[slot]
