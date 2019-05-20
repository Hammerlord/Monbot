from random import random
from typing import List

from src.elemental.combat_elemental import CombatElemental
from src.elemental.elemental import Elemental
from src.elemental.species.felix import Felix
from src.elemental.species.mithus import Mithus
from src.elemental.species.nepharus import Nepharus
from src.elemental.species.noel import Noel
from src.elemental.species.npc_monsters.manapher import Manapher
from src.elemental.species.npc_monsters.tophu import Tophu
from src.elemental.species.rainatu import Rainatu
from src.elemental.species.rex import Rex
from src.elemental.species.roaus import Roaus
from src.elemental.species.sithel import Sithel
from src.elemental.species.slyfe import Slyfe
from src.items.consumables import Peach, Cake, Pudding, Meat
from src.items.shards import *


class Loot:
    """
    An item dropped by an Elemental upon knock-out.
    """

    def __init__(self,
                 item,
                 drop_rate: float = 1):
        """
        :param item: Item
        :param drop_rate: The percentage chance that this item will drop upon combat resolution.
        """
        self.item = item
        self.drop_rate = drop_rate


loot_table = {
    Felix.name: [
        Loot(ManaShard, 0.5),
        Loot(Peach, 0.75),
        Loot(Cake, 0.5),
        Loot(Pudding, 0.2)
    ],
    Mithus.name: [
        Loot(ManaShard, 0.5),
        Loot(Meat, 0.5),
    ],
    Nepharus.name: [
        Loot(Peach, 0.8),
        Loot(Cake, 0.3),
        Loot(ManaShard, 0.5)
    ],
    Noel.name: [
        Loot(Meat, 0.5),
        Loot(ManaShard, 0.5),
        Loot(Pudding, 0.1)
    ],
    Rainatu.name: [
        Loot(Peach, 0.8),
        Loot(ManaShard, 0.5),
        Loot(Cake, 0.3)
    ],
    Rex.name: [
        Loot(Meat, 0.8),
        Loot(ManaShard, 0.5)
    ],
    Manapher.name: [
        Loot(Peach),
        Loot(ManaShard)
    ],
    Roaus.name: [
        Loot(Peach, 0.8),
        Loot(ManaShard, 0.5)
    ],
    Sithel.name: [
        Loot(Peach, 0.8),
        Loot(ManaShard, 0.5)
    ],
    Slyfe.name: [
        Loot(Peach, 0.8),
        Loot(ManaShard, 0.5)
    ],
    Tophu.name: [
        Loot(Peach()),
        Loot(ManaShard())
    ]
}


def roll_elemental_shard(elemental_type: Elements) -> Shard or None:
    if random() > 0.75:
        return
    for shard in [EarthShard, LightningShard, FireShard, WaterShard, WindShard, ShadowShard, LightShard, ChaosShard]:
        if shard.element == elemental_type:
            return shard


def roll_loot(elemental: CombatElemental) -> List[Item]:
    items: List[Item] = []
    if elemental.name in loot_table:
        for loot in loot_table[elemental.name]:
            if random() <= loot.drop_rate:
                items.append(loot.item)
    else:
        print(f"{elemental.name} doesn't have a specific loot table.")
    shard = roll_elemental_shard(elemental.element)
    if shard:
        items.append(shard)
    return items
