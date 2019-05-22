import random

from src.character.npc.npc_initializer import NPCInitializer
from src.character.player import Player
from src.combat.combat import Combat
from src.data.data_manager import DataManager
from src.elemental.elemental_factory import ElementalInitializer
from src.elemental.species.npc_monsters.manapher import Manapher
from src.elemental.species.npc_monsters.tophu import Tophu
from src.team.combat_team import CombatTeam


class BattleManager:
    """
    How a user enters combat.
    """

    @staticmethod
    def create_duel(player: Player, other_player: Player) -> None:
        """
        Start a fight between two players.
        """
        Combat([CombatTeam.from_team(player.team)],
               [CombatTeam.from_team(other_player.team)],
               data_manager=DataManager(),
               allow_flee=False,
               allow_items=False)

    @staticmethod
    def create_pve_combat(player: Player) -> CombatTeam:
        if player.battles_fought < 2:
            opponent = BattleManager._tutorial_opponent(player)
        else:
            opponent = BattleManager._get_random_opponent(player)
        player_team = CombatTeam.from_team(player.team)
        Combat([player_team],
               [opponent],
               data_manager=DataManager())
        return player_team

    @staticmethod
    def _tutorial_opponent(player: Player) -> CombatTeam:
        if player.battles_fought == 0:
            tutorial_elemental = Tophu()
        else:
            tutorial_elemental = Manapher()
        return CombatTeam([ElementalInitializer.make(tutorial_elemental)])

    @staticmethod
    def _get_random_opponent(player: Player) -> CombatTeam:
        """
        A random encounter with an Elemental or NPC.
        """
        coin_flip = random.randint(0, 1)
        if coin_flip:
            opponent = NPCInitializer().get_random_opponent()
            opponent.generate_team(player)
            return CombatTeam.from_team(opponent.team)
        return BattleManager._get_wild_elemental(player)

    @staticmethod
    def _get_wild_elemental(player: Player) -> CombatTeam:
        team_average = player.team.average_elemental_level
        min_level = team_average - 1
        max_level = team_average + player.team.size
        level = random.randint(min_level, max_level)
        return CombatTeam([ElementalInitializer.make_random(level)])
