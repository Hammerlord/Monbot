from src.core.constants import PEACH, HAMMER, MANA_SHARD, CAKE, PUDDING, MEAT
from src.items.item import Item, ItemTypes


class Consumable(Item):
    item_type = ItemTypes.CONSUMABLE
    healing_percentage: float
    exp_gained_on_use: int
    resurrects_target: bool

    @staticmethod
    def generate_properties(consumable: 'Consumable') -> str:
        """
        TODO this shouldn't really be here
        :return: A string displaying the various properties of a consumable for rendering purposes.
        """
        properties = []
        if consumable.resurrects_target:
            properties.append("[Revives KO]")
        if consumable.healing_percentage > 0:
            properties.append(f"[+{int(consumable.healing_percentage * 100)}% HP]")
        if consumable.exp_gained_on_use > 0:
            properties.append(f"[+{consumable.exp_gained_on_use} EXP]")
        return ' '.join(properties)

    @staticmethod
    def is_usable_on(target) -> bool:
        """
        :param target: Elemental or CombatElemental
        """
        raise NotImplementedError

    @staticmethod
    def use_on(target) -> None:
        """
        :param target: Elemental or CombatElemental
        """
        raise NotImplementedError


class Peach(Consumable):
    name = 'Peach'
    description = 'A ripe and juicy peach.'
    icon = PEACH
    healing_percentage = 0.35
    exp_gained_on_use = 5
    buy_price = 3
    sell_price = 1
    resurrects_target = False

    @staticmethod
    def is_usable_on(target):
        return not target.is_knocked_out

    @staticmethod
    def use_on(target) -> None:
        """
        :param target: Elemental or CombatElemental
        """
        heal_amount = target.max_hp * Peach.healing_percentage
        target.heal(heal_amount)
        target.add_exp(Peach.exp_gained_on_use)


class Revive(Consumable):
    name = 'Revive'
    description = 'Revive a knocked-out elemental.'
    icon = HAMMER
    healing_percentage = 0.2
    exp_gained_on_use = 0
    buy_price = 10
    sell_price = 5
    resurrects_target = True

    @staticmethod
    def is_usable_on(target):
        return target.is_knocked_out

    @staticmethod
    def use_on(target) -> None:
        """
        :param target: Elemental or CombatElemental
        """
        heal_amount = target.max_hp * Revive.healing_percentage
        target.heal(heal_amount)


class Cake(Consumable):
    name = 'Slice of Cake'
    description = 'A delicious frosted cake topped with a strawberry.'
    icon = CAKE
    healing_percentage = 0.5
    exp_gained_on_use = 15
    buy_price = 8
    sell_price = 5
    resurrects_target = False

    @staticmethod
    def is_usable_on(target):
        return not target.is_knocked_out

    @staticmethod
    def use_on(target) -> None:
        """
        :param target: Elemental or CombatElemental
        """
        heal_amount = target.max_hp * Cake.healing_percentage
        target.heal(heal_amount)
        target.add_exp(Cake.exp_gained_on_use)


class Meat(Consumable):
    name = 'Meat on Bone'
    description = 'Succulent meat on a bone. Makes a hearty meal.'
    icon = MEAT
    healing_percentage = 0.7
    exp_gained_on_use = 20
    buy_price = 25
    sell_price = 8
    resurrects_target = False

    @staticmethod
    def is_usable_on(target):
        return not target.is_knocked_out

    @staticmethod
    def use_on(target) -> None:
        """
        :param target: Elemental or CombatElemental
        """
        heal_amount = target.max_hp * Meat.healing_percentage
        target.heal(heal_amount)
        target.add_exp(Meat.exp_gained_on_use)


class Pudding(Consumable):
    name = 'Pudding'
    description = 'A mango pudding with a chocolate top.'
    icon = PUDDING
    healing_percentage = 0.2
    exp_gained_on_use = 150
    buy_price = 50
    sell_price = 20
    resurrects_target = False

    @staticmethod
    def is_usable_on(target):
        return not target.is_knocked_out

    @staticmethod
    def use_on(target) -> None:
        """
        :param target: Elemental or CombatElemental
        """
        heal_amount = target.max_hp * Pudding.healing_percentage
        target.heal(heal_amount)
        target.add_exp(Pudding.exp_gained_on_use)