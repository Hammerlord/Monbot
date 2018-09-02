from src.character.character import Character
from src.character.consumables import Peach, Revive
from src.ui.forms.form import Form


class Player(Character):
    def __init__(self, user):
        super().__init__()
        self._level = 30
        self.primary_view = None  # Type: Form
        self.combat_team = None  # Type: CombatTeam
        self._challenges = {}  # {discord.message.id: ChallengeForm}: A map of all the challenges issued to this Player.
        self.id = user.id
        self._nickname = user.name
        self.battles_fought = 0
        self._gold = 5
        self.inventory.add_item(Peach(), 2)
        self.inventory.add_item(Revive(), 1)

    def __eq__(self, other):
        return self.team.average_elemental_level == other.team.average_elemental_level

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

    def set_combat_team(self, combat) -> None:
        self.combat_team = combat
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
