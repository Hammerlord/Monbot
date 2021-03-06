from random import randint

from src.character.character import Character
from src.character.player import Player
from src.elemental.elemental import Elemental
from src.elemental.elemental_factory import ElementalInitializer
from src.elemental.species.species import Species


class NPC(Character):
    """
    A non-player character with a Team of Elementals that a Player can battle.
    The profession of NPCs influence what Elementals appear on their Team.
    """

    def __init__(self,
                 nickname: str,
                 potential_species):
        """
        :param nickname: Eg. 'Adventurer'
        :param potential_species: List[Species]
        """
        super().__init__()
        self._is_npc = True
        self._nickname = nickname
        self._potential_species = potential_species

    def generate_equal_team(self, opponent: 'Character') -> None:
        """
        Generates a randomized Team that has the same number of Elementals as the opponent.
        :param opponent:
        :return:
        """
        self._level = opponent.level
        for i in range(opponent.team.size):
            elemental = self._get_random_elemental()
            self._team.add_elemental(elemental)

    def generate_team(self, opponent: 'NPC' or Player) -> None:
        """
        Generates a randomized Team based on the opponent's level and Team size.
        """
        self._generate_level(opponent)
        team_size = self._roll_team_size(opponent)
        for i in range(team_size):
            elemental = self._get_random_elemental()
            self._team.add_elemental(elemental)

    def generate_random_team(self,
                             min_level=1,
                             max_level=60,
                             min_team_size=1,
                             max_team_size=4):
        """
        Generates a random Team, not based off of an opponent.
        """
        self._level = randint(min_level, max_level)
        team_size = randint(min_team_size, max_team_size)
        for i in range(team_size):
            elemental = self._get_random_elemental()
            self._team.add_elemental(elemental)

    def _generate_level(self, opponent: 'NPC' or Player) -> None:
        """
        :param opponent: This NPC's upcoming opponent, usually a Player.
        When called, the NPC's level will be based off of the opponent's average team level.
        """
        team_average_level = opponent.team.average_elemental_level
        min_level = max(1, team_average_level - 3)  # Cannot be below 1
        max_level = team_average_level + 1
        self._level = randint(min_level, max_level)

    @staticmethod
    def _roll_team_size(opponent: 'NPC' or Player) -> int:
        """
        Generates a Team size that is not larger than the opponent's.
        """
        min_team_size = 1
        max_team_size = opponent.team.size
        return randint(min_team_size, max_team_size)

    def _get_random_elemental(self) -> 'Elemental':
        species = self._get_random_species()
        level = self._roll_elemental_level()
        return ElementalInitializer().make(species, level)

    def _roll_elemental_level(self) -> int:
        min_level = max(1, self._level - 2)  # Cannot be below 1
        max_level = self._level
        return randint(min_level, max_level)

    def _get_random_species(self) -> 'Species':
        """
        :return: Species, the static information about an Elemental.
        """
        pick = randint(0, len(self._potential_species) - 1)
        return self._potential_species[pick]
