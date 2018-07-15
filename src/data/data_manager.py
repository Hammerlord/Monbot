from src.character.player import Player


class DataManager:
    def __init__(self):
        self.players = {}  # TODO stored data

    def get_player(self, user) -> Player or None:
        if user.id not in self.players:
            self._create_profile(user)
        return self.players[user.id]

    def _create_profile(self, user) -> None:
        new_player = Player(user)
        self.players[user.id] = new_player