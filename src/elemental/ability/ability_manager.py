from typing import List

from src.elemental.ability.ability import LearnableAbility
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
    def active_abilities(self) -> List[LearnableAbility]:
        """
        :return: Abilities usable in combat by the Elemental.
        """
        return self._active_abilities

    @property
    def available_abilities(self) -> List[LearnableAbility]:
        """
        :return: Abilities that have been learned by the Elemental.
        """
        return self._available_abilities

    @property
    def eligible_abilities(self) -> List[LearnableAbility]:
        """
        :return: Available abilities that are not already in active abilities.
        """
        return [ability for ability in self._available_abilities if ability not in self._active_abilities]

    def check_learnable_abilities(self) -> None:
        """
        Check the requirements of the learnable abilities, and add them to the "available" container.
        """
        for ability in self._learnable_abilities:
            if self._can_learn(ability):
                self._learn_ability(ability)

    def swap_ability(self, active_position: int, available_position: int) -> None:
        """
        Replaces a LearnableAbility in active_abilities with one from available_abilities.
        Uses position in the respective lists.
        """
        self._active_abilities[active_position] = self.eligible_abilities[available_position]

    def _can_learn(self, ability: LearnableAbility) -> bool:
        return ability.are_requirements_fulfilled(self.elemental) \
               and ability not in self._available_abilities

    def _learn_ability(self, ability: LearnableAbility) -> None:
        if len(self._active_abilities) < self._max_active:
            self._active_abilities.append(ability)
        self._available_abilities.append(ability)

    def _initialize_abilities(self) -> List[LearnableAbility]:
        abilities = self.elemental.species.learnable_abilities
        abilities.append(AbilityFactory.defend())  # All Elementals learn Defend
        return abilities