from src.core.constants import DEFEND
from src.elemental.status_effect.status_effect import StatusEffect, EffectType


class DefendEffect(StatusEffect):
    """
    The status effect applied by Defend, which grants the CombatElemental damage reduction
    equal to its own Defend Potency until the end of the round.
    """
    def __init__(self):
        super().__init__()
        self.icon = DEFEND
        self.effect_type = EffectType.DEFEND

    @property
    def damage_reduction(self) -> float:
        return self.target.defend_potency

    @property
    def turn_duration(self) -> int:
        """
        This ability should last until the end of the round, hence it is unaffected by turns.
        """
        return -1

    @property
    def round_duration(self) -> int:
        """
        Lasts until the end of the round.
        """
        return 1