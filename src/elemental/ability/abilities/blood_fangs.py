from src.core.elements import Elements, Category
from src.elemental.ability.ability import Ability, Target


class BloodFangs(Ability):
    def __init__(self):
        super().__init__()
        self.name = "Blood Fangs"
        self._description = (f"Lash out at an enemy and regain {self.actor_recovery*100}% HP. "
                             f"Damage and healing increased up to 2x based on missing health.")
        self.element = Elements.DARK
        self.category = Category.PHYSICAL
        self.attack_power = 15
        self.actor_recovery = 0.1
        self.mana_cost = 15
        self.defend_cost = 0
        self.targeting = Target.ENEMY

    @staticmethod
    def get_bonus_multiplier(target, actor) -> float:
        missing_health = (actor.max_hp - actor.current_hp) / actor.max_hp
        return 1 + missing_health
