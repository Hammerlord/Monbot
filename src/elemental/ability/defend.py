from src.elemental.ability.ability import Ability, Target
from src.elemental.status_effect.status_effect import StatusEffect


class DefendEffect(StatusEffect):

    def __init__(self):
        super().__init__()
        self._icon = ':shield:'

    @property
    def _base_duration(self) -> float:
        return 0.5  # Until the end of the opponent's turn

    def on_effect_start(self) -> None:
        self.apply_stat_changes()

    def on_receive_damage(self, amount: int, actor) -> str:
        return f"{self.target.nickname} is defending!"

    def apply_stat_changes(self) -> None:
        self.target.update_damage_reduction(self.target.defend_potency)


class Defend(Ability):
    def __init__(self):
        super().__init__()
        self.id = 1
        self.name = "Defend"
        self.description = "Block incoming damage until the next turn. Gain +10 mana."
        self.turn_priority = 1
        self.targeting = Target.SELF

    def execute(self, target: 'CombatElemental'):
        target.add_status_effect(DefendEffect())
