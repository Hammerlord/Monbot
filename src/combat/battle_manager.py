from src.character.player import Player
from src.combat.combat import Combat
from src.elemental.elemental_factory import ElementalInitializer
from src.team.combat_team import CombatTeam


class BattleManager:
    """
    How a user enters combat.
    """

    @staticmethod
    def dummy_fight(player_team: CombatTeam) -> Combat:
        combat = Combat()
        combat.join_battle(player_team)
        opponent = CombatTeam.from_elementals([ElementalInitializer.manapher()])
        combat.join_battle(opponent)
        return combat