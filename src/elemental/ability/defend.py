from src.elemental.ability.ability import Ability
from src.elemental.status_effect.status_effect import StatusEffect


class DefendEffect(StatusEffect):
    def __init__(self):
        super().__init__()
        self._max_duration = 2  # TODO doesn't end until end of next turn

    def on_effect_start(self):
        self.apply_stat_changes()

    def apply_stat_changes(self):
        self.target.update_damage_reduction(self.target.defend_potency)

    def get_recap(self) -> str:
        return f"{self.target.nickname} is defending!"


class Defend(Ability):
    def __init__(self):
        super().__init__()
        self.id = 1
        self.name = "Defend"
        self.description = "Block incoming damage until the next turn. Gain +10 mana."
        self.turn_priority = 1

    def execute(self, target: 'CombatElemental'):
        target.add_status_effect(DefendEffect())
