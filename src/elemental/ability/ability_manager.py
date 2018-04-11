from typing import List

from src.elemental.ability.ability import LearnableAbility, Ability
from src.elemental.ability.ability_factory import AbilityFactory


class AbilityManager:
    def __init__(self, elemental):
        """
        :param elemental: The Elemental to whom this Manager belongs.
        """
        self.elemental = elemental
        self._learnable_abilities = self._initialize_abilities()  # List[LearnableAbility]
        self._available_abilities = []
        self._active_abilities = []
        self._max_active = 5
        self.check_learnable_abilities()

    @property
    def active_abilities(self) -> List[Ability]:
        """
        :return: Abilities usable in combat by the Elemental.
        """
        return self._active_abilities

    @property
    def available_abilities(self) -> List[Ability]:
        """
        :return: Abilities that have been learned by the Elemental.
        """
        return self._available_abilities

    @property
    def eligible_abilities(self) -> List[Ability]:
        """
        :return: Available abilities that are not already in active abilities.
        Eg. for presenting options when swapping abilities.
        """
        return [ability for ability in self._available_abilities if ability not in self._active_abilities]

    def check_learnable_abilities(self) -> None:
        """
        Check the requirements of learnable abilities, and add any which have been fulfilled
        to the "available" container. Extracts the Ability object from the LearnableAbility.
        """
        for learnable_ability in self._learnable_abilities:
            if self._can_learn(learnable_ability):
                self._learn_ability(learnable_ability)

    def swap_ability(self, active_position: int, available_position: int) -> None:
        """
        Replaces an Ability in active_abilities with one from eligible_abilities.
        Uses position in the respective lists.
        """
        if self._active_abilities[active_position].id == 1:
            # Defend, which is ability id 1, is not swappable.
            return
        self._active_abilities[active_position] = self.eligible_abilities[available_position]

    def _can_learn(self, learnable_ability: LearnableAbility) -> bool:
        not_yet_learned = learnable_ability.ability not in self._available_abilities
        return not_yet_learned and learnable_ability.are_requirements_fulfilled(self.elemental)

    def _learn_ability(self, learnable_ability: LearnableAbility) -> None:
        ability = learnable_ability.ability
        if len(self._active_abilities) < self._max_active:
            self._active_abilities.insert(0, ability)  # Keep Defend last in the list.
        self._available_abilities.append(ability)

    def _initialize_abilities(self) -> List[LearnableAbility]:
        abilities = self.elemental.species.learnable_abilities
        abilities.insert(0, AbilityFactory.defend())  # All Elementals learn Defend
        return abilities
