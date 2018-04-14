from src.character.character import Character
from src.character.npc import NPC
from src.character.npc_initializer import NPCInitializer
from src.character.player import Player
from tests.character.test_user import UserBuilder
from tests.elemental.elemental_builder import ElementalBuilder


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
        self._opponent = PlayerBuilder().build()

    def build(self) -> NPC:
        npc = NPCInitializer.adventurer()
        npc.generate_team(self._opponent)
        return npc

    def with_opponent(self, opponent: NPC or Player) -> 'NPCBuilder':
        self._opponent = opponent
        return self


class PlayerBuilder:
    def __init__(self):
        self._level = 1
        self.user = UserBuilder().build()

    def build(self) -> Player:
        player = Player(self.user)
        player.add_elemental(ElementalBuilder().build())
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
