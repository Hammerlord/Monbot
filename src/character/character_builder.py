from typing import Type

from src.character.character import Character
from src.character.npc import NPC
from src.character.player import Player
from tests.test_user import UserBuilder


class CharacterBuilder:
    def __init__(self):
        self._level = 1

    def build(self) -> Character:
        character = Character()
        while character.level < self._level:
            exp = character.exp_to_level
            character.add_exp(exp)
        return character

    def with_level(self, level: int) -> 'CharacterBuilder':
        self._level = level
        return self


class NPCBuilder:
    def __init__(self):
        self._level = 1
        self.opponent = PlayerBuilder().build()

    def build(self) -> NPC:
        npc = NPC()
        while npc.level < self._level:
            exp = npc.exp_to_level
            npc.add_exp(exp)
        return npc

    def with_level(self, level: int) -> 'NPCBuilder':
        self._level = level
        return self

    def with_opponent(self, opponent: NPC or Player) -> 'NPCBuilder':
        self.opponent = opponent
        return self


class PlayerBuilder:
    def __init__(self):
        self._level = 1
        self.user = UserBuilder().build()

    def build(self) -> Player:
        player = Player(self.user)
        while player.level < self._level:
            exp = player.exp_to_level
            player.add_exp(exp)
        return player

    def with_level(self, level: int) -> 'PlayerBuilder':
        self._level = level
        return self

    def with_user(self, user) -> 'PlayerBuilder':
        self.user = user
        return self
