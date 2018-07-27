from src.core.elements import Elements, Category
from src.elemental.ability.ability import Ability, Target


class Geyser(Ability):

    def __init__(self):
        super().__init__()
        self.name = "Geyser"
        self._description = "Blast an opponent with a torrent of water."
        self.element = Elements.WATER
        self.category = Category.MAGIC
        self.attack_power = 22
        self.mana_cost = 15
        self.defend_cost = 0
        self.targeting = Target.ENEMY