from src.character.character import Character
from src.character.npc.npc import NPC
from src.character.npc.npc_initializer import NPCInitializer
from src.character.player import Player
from tests.character.user_builder import UserBuilder
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

    def with_max_level(self) -> 'CharacterBuilder':
        self._level = Character.MAX_LEVEL
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
        self.elementals = [ElementalBuilder().build()]
        self._nickname = None

    def build(self) -> Player:
        player = Player(self.user.id, self.user.name)
        if self._nickname:
            player.nickname = self._nickname
        for elemental in self.elementals:
            player.add_elemental(elemental)
        while player.level < self._level:
            exp = player.exp_to_level
            player.add_exp(exp)
        return player

    def with_elementals(self, elementals: list) -> 'PlayerBuilder':
        self.elementals = elementals
        return self

    def with_level(self, level: int) -> 'PlayerBuilder':
        self._level = level
        return self

    def with_nickname(self, nickname: str) -> 'PlayerBuilder':
        self._nickname = nickname
        return self

    def with_user(self, user) -> 'PlayerBuilder':
        self.user = user
        return self
