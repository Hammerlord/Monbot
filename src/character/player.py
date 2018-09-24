from src.character.character import Character
from src.data.resources import PlayerResource, InventoryResource
from src.items.consumables import Peach, Revive
from src.ui.forms.form import Form


class Player(Character):
    def __init__(self,
                 id: str,
                 name: str,
                 level=1,
                 current_exp=0,
                 gold=5,
                 battles_fought=0,
                 location=0):
        super().__init__()
        self._level_to(level)
        self._current_exp = current_exp
        self._check_level_up()
        self.primary_view = None  # Type: Form
        self.combat_team = None  # Type: CombatTeam
        self._challenges = {}  # {discord.message.id: ChallengeForm}: A map of all the challenges issued to this Player.
        self.id = id
        self._nickname = name
        self.battles_fought = battles_fought
        self._gold = gold
        self.location = location  # TODO

    def add_starter_items(self):
        self.inventory.add_item(Peach(), 2)
        self.inventory.add_item(Revive(), 1)

    @staticmethod
    def from_user(user) -> 'Player':
        return Player(user.id, user.name)

    @staticmethod
    def from_resource(resource: PlayerResource) -> 'Player':
        """
        Load a player from server data. Elementals and inventory handled separately.
        """
        return Player(resource.id,
                      resource.name,
                      resource.level,
                      resource.current_exp,
                      resource.gold,
                      resource.battles_fought,
                      resource.location)

    def __lt__(self, other):
        return self.team.average_elemental_level < other.team.average_elemental_level

    @property
    def can_battle(self) -> bool:
        return not self.is_busy and not self.team.is_all_knocked_out

    def has_item(self, item) -> bool:
        return self.inventory.has_item(item)

    @property
    def has_elemental(self) -> bool:
        return len(self.elementals) > 0

    def set_elementals(self, elementals) -> None:
        """
        :param elementals: List[Elemental]
        """
        for elemental in elementals:
            self.add_elemental(elemental)

    def set_team(self, elementals) -> None:
        """
        :param elementals: List[Elemental]
        """
        self._team.set(elementals)

    def set_primary_view(self, view: Form) -> None:
        self.primary_view = view

    @property
    def view_message(self):
        """
        :return: Discord message object.
        This is how the view actually gets represented in Discord.
        """
        return self.primary_view.discord_message

    @property
    def is_busy(self) -> bool:
        """
        :return: True if the player is in combat and therefore has a CombatTeam.
        """
        return self.combat_team is not None

    def set_combat_team(self, combat_team) -> None:
        self.combat_team = combat_team
        self.battles_fought += 1

    def clear_combat(self) -> None:
        self.combat_team = None

    def add_challenge(self, challenge) -> None:
        """
        :param challenge: ChallengeForm: Record the challenge issued to this Player.
        """
        self._challenges[challenge.discord_message.id] = challenge

    def get_challenge(self, message):
        """
        :param message: discord.message
        :return: ChallengeForm or None
        """
        if message.id in self._challenges:
            return self._challenges[message.id]

    def remove_challenge(self, challenge) -> None:
        if challenge.discord_message.id in self._challenges:
            del self._challenges[challenge.discord_message.id]

    def clear_challenges(self) -> None:
        for challenge in self._challenges:
            challenge.cancel()
        self._challenges = {}

    def to_server(self) -> dict:
        """
        Return a structure uploadable to the server.
        """
        return PlayerResource(
            id=self.id,
            name=self._nickname,
            level=self._level,
            current_exp=self.current_exp,
            gold=self.gold,
            battles_fought=self.battles_fought,
            team=[elemental.id for elemental in self.team.elementals],
            elementals=[elemental.id for elemental in self.elementals],
            location=self.location
        )._asdict()

    def inventory_to_server(self) -> dict:
        return InventoryResource(
            id=self.id,
            items=self.inventory.to_server()
        )._asdict()

    def _level_to(self, level: int) -> None:
        while self.level < int(level):
            self._level += 1
            self._increase_exp_to_level()
