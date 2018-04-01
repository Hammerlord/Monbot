from src.character.character import Character


class CharacterBuilder:
    def __init__(self):
        self.character = Character()

    def build(self) -> Character:
        return self.character

    def with_level(self, level: int) -> 'CharacterBuilder':
        while self.character.get_level() < level:
            exp = self.character.get_exp_to_level()
            self.character.add_exp(exp)
        return self

