from typing import List

from src.combat.combat_actions import KnockedOut, ElementalAction, Switch
from src.elemental.ability.ability import Ability
from src.elemental.combat_elemental import CombatElemental
from src.team.team import Team


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
        self._actions = []  # list[Action] taken by this team.
        self.turn_log = []  # list[list[str]], detailing status effects at each stage of the turn, actions...

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

    @property
    def last_action(self):
        previous = len(self._actions) - 1
        return self._actions[previous]

    def use_ability(self, ability: Ability) -> None:
        if self.active.is_knocked_out:
            self.handle_knockout()
        else:
            self.make_action(ability)
            self.end_turn()
        self.combat.check_end()

    def end_turn(self) -> None:
        self.active.on_turn_end()
        # Check knocked out again in case a debuff, etc. finished off the Elemental
        if self.active.is_knocked_out:
            self.handle_knockout()

    def handle_knockout(self) -> None:
        self._actions.append(KnockedOut(self._active))

    def make_action(self, ability: Ability) -> None:
        """
        Execute the Ability and create a log for it.
        """
        action = ElementalAction(
            character=self.owner,
            actor=self.active,
            ability=ability,
            target=self.combat.get_target(ability, self.active)
        )
        action.execute()
        self._actions.append(action)
        self._active.add_action(action)

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
        valid_slot = 0 <= slot < len(eligible_elementals)  # Valid slot?
        if not valid_slot:
            return
        self._actions.append(Switch(
            character=self.owner,
            old_active=self.active,
            new_active=eligible_elementals[slot]
        ))
        self._active = eligible_elementals[slot]
