import random
from collections import namedtuple

from src.character.npc_initializer import NPCInitializer
from src.character.player import Player
from src.combat.combat import Combat
from src.elemental.elemental_factory import ElementalInitializer
from src.elemental.species.manapher import Manapher
from src.team.combat_team import CombatTeam


class BattleManager:
    """
    How a user enters combat.
    """

    @staticmethod
    def tutorial_fight() -> Combat:
        combat = Combat()
        opponent = CombatTeam.from_elementals([ElementalInitializer.make(Manapher())])
        combat.join_battle(opponent)
        return combat

    def get_fight(self, player: Player):
        player_team = CombatTeam(player.team)
        if player.battles_fought == 0:
            combat = self.tutorial_fight()
        else:
            combat = self.get_random_fight(player)
        combat.join_battle(player_team)
        options = namedtuple('Options', 'combat, player_team')
        return options(combat, player_team)

    @staticmethod
    def get_random_fight(player: Player) -> Combat:
        """
        A random encounter with an Elemental or NPC.
        """
        coin_flip = random.randint(0, 1)
        combat = Combat()
        if coin_flip:
            opponent = NPCInitializer().collector()
            opponent.generate_team(player)
            opponent_team = CombatTeam(opponent.team)
        else:
            opponent_team = CombatTeam.from_elementals([ElementalInitializer.make_random(player.level)])
        combat.join_battle(opponent_team)
        return combat
