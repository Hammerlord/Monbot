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
        combat = Combat(data_manager=DataManager(),
                        allow_flee=False,
                        allow_items=False)
        player_team = CombatTeam(player.team)
        other_player_team = CombatTeam(other_player.team)
        combat.join_battle(player_team)
        combat.join_battle(other_player_team)

    def create_pve_combat(self, player: Player) -> CombatTeam:
        if player.battles_fought < 2:
            combat = self._tutorial_fight(player)
        else:
            combat = self._get_random_fight(player)
        player_team = CombatTeam(player.team)
        combat.join_battle(player_team)
        return player_team

    @staticmethod
    def _tutorial_fight(player: Player) -> Combat:
        if player.battles_fought == 0:
            tutorial_elemental = Tophu()
        else:
            tutorial_elemental = Manapher()
        combat = Combat(data_manager=DataManager())
        opponent = CombatTeam.from_elementals([ElementalInitializer.make(tutorial_elemental)])
        combat.join_battle(opponent)
        return combat

    @staticmethod
    def _get_random_fight(player: Player) -> Combat:
        """
        A random encounter with an Elemental or NPC.
        """
        coin_flip = random.randint(0, 1)
        if coin_flip:
            opponent = NPCInitializer().get_random_opponent()
            opponent.generate_team(player)
            opponent_team = CombatTeam(opponent.team)
        else:
            opponent_team = BattleManager._get_wild_elemental(player)
        combat = Combat(data_manager=DataManager())
        combat.join_battle(opponent_team)
        return combat

    @staticmethod
    def _get_wild_elemental(player: Player) -> CombatTeam:
        team_average = player.team.average_elemental_level
        min_level = team_average - 1
        max_level = team_average + player.team.size
        level = random.randint(min_level, max_level)
        return CombatTeam.from_elementals([ElementalInitializer.make_random(level)])