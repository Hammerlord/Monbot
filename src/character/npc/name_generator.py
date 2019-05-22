import random
from enum import Enum
from typing import List

from trepan.processor.command.base_submgr import capitalize

from src.character.npc.name_syllables import *


class Races(Enum):
    LOWLANDER = 'Lowlander'
    HIGHLANDER = 'Highlander'
    REDIN = 'Redin'
    TIGRUN = 'Tigrun'
    UMRIN = 'Umrin'
    RIKELRIN = 'Rikelrin'
    RYAS = 'Ryas'


race_syllables_map = {
    Races.LOWLANDER: LOWLANDER_SYLLABLES,
    Races.HIGHLANDER: HIGHLANDER_SYLLABLES,
    Races.REDIN: REDIN_SYLLABLES,
    Races.TIGRUN: TIGRUN_SYLLABLES,
    Races.UMRIN: UMRIN_SYLLABLES,
    Races.RIKELRIN: RIKELRIN_SYLLABLES,
    Races.RYAS: RYAS_SYLLABLES
}


def pick_random(from_list) -> any:
    index = random.randint(0, len(from_list) - 1)
    return from_list[index]


class NameGenerator:

    @staticmethod
    def generate_name() -> str:
        syllables = pick_random(list(race_syllables_map.values()))
        name = NameGenerator._construct_name(syllables)
        for filtered in FILTER:
            if filtered in name:
                name = NameGenerator._construct_name(syllables)  # Reroll once for now.
                break
        return capitalize(name)

    @staticmethod
    def _construct_name(syllables: List[str]) -> str:
        syllables = list(syllables)  # Defensive copy due to popping
        name = []
        num_components = pick_random([1, 2, 2, 3])
        for i in range(num_components):
            index = random.randint(0, len(syllables) - 1)
            component = syllables.pop(index)
            name.append(component)
        return ''.join(name)


FILTER = ['hair', 'naan', 'seinen', 'feilun', 'wonka', 'anal', 'shit', 'lol', 'groan', 'shota',
          'futa', 'satan', 'nerdy', 'renal', 'greed', 'strong', 'ass', 'genome', 'mister', 'kinky', 'india',
          'oo', 'bored']
