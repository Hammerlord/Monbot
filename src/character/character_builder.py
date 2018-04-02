from src.character.character import Character
from src.character.npc import NPC
from src.character.player import Player


class CharacterBuilder:
    def __init__(self):
        self.character = Character()

    def build(self) -> Character:
        return self.character

    def with_level(self, level: int) -> 'CharacterBuilder':
        while self.character.level < level:
            exp = self.character.exp_to_level
            self.character.add_exp(exp)
        return self


class NPCBuilder:
    def __init__(self):
        self.npc = NPC()

    def build(self) -> NPC:
        return self.npc

    def with_level(self, level: int) -> 'NPCBuilder':
        while self.npc.level < level:
            exp = self.npc.exp_to_level
            self.npc.add_exp(exp)
        return self

    def with_opponent(self, player: Player) -> 'NPCBuilder':
        self.npc.generate_team(player)
        return self
