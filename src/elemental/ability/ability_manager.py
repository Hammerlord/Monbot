from typing import List

from src.elemental.ability.ability import LearnableAbility, Ability
from src.elemental.ability.ability_factory import LearnableAbilities


class AbilityManager:
    def __init__(self, elemental):
        """
        :param elemental: The Elemental to whom this Manager belongs.
        """
        self.elemental = elemental
        self._learnable_abilities = self._initialize_abilities()  # List[LearnableAbility]
        self._available_abilities = []
        self._active_abilities = []
        self._total_active_abilities = 5
        self.check_learnable_abilities()

    @property
    def max_active_abilities(self) -> int:
        # Excluding Defend.
        return self._total_active_abilities - 1

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
        return list(self._available_abilities)

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

    def set_abilities_from_names(self, ability_names: List[str]) -> None:
        name_map = {}
        for ability in self._available_abilities:
            name_map[ability.name] = ability
        self._active_abilities = []
        for name in ability_names:
            self._active_abilities.append(name_map[name])

    def set_abilities(self, abilities: List[Ability]) -> None:
        """
        Be lenient when setting excessive abilities (however that may happen) but reject sets that aren't full.
        :param abilities: To replace currently active abilities.
        """
        if len(abilities) < self.max_active_abilities:
            return
        defend = next(ability for ability in self.active_abilities if ability.name == 'Defend')
        self._active_abilities = []
        for i in range(self.max_active_abilities):
            self._active_abilities.append(abilities[i])
        # Defend is a part of every Elemental's toolkit.
        self._active_abilities.append(defend)

    def swap_ability(self, active_ability: Ability, eligible_ability: Ability) -> None:
        """
        Replaces an Ability in active_abilities with one from eligible_abilities.
        """
        if active_ability.name == "Defend":
            # Defend is not swappable. This shouldn't ever be reached anyway.
            return
        index = self._active_abilities.index(active_ability)
        self._active_abilities[index] = eligible_ability

    def find_ability_by_name(self, name: str) -> Ability or None:
        for ability in self._available_abilities:
            if ability.name == name:
                return ability

    def _can_learn(self, learnable_ability: LearnableAbility) -> bool:
        not_yet_learned = learnable_ability.ability not in self._available_abilities
        return not_yet_learned and learnable_ability.are_requirements_fulfilled(self.elemental)

    def _learn_ability(self, learnable_ability: LearnableAbility) -> None:
        ability = learnable_ability.ability
        if len(self._active_abilities) < self._total_active_abilities:
            self._active_abilities.insert(0, ability)  # Keep Defend last in the list.
        self._available_abilities.append(ability)

    def _initialize_abilities(self) -> List[LearnableAbility]:
        abilities = self.elemental.species.learnable_abilities
        abilities.insert(0, LearnableAbilities.defend())  # All Elementals learn Defend
        return abilities
