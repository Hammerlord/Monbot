from typing import NamedTuple, List


class AttributesResource(NamedTuple):
    name: str
    level: int


class ElementalResource(NamedTuple):
    id: str
    level: int
    current_hp: int
    current_exp: int
    species: str
    active_abilities: List[str]
    attributes: List[AttributesResource]


class ItemResource(NamedTuple):
    name: str
    amount: int


class InventoryResource(NamedTuple):
    id: str
    items: List[ItemResource]


class PlayerResource(NamedTuple):
    id: str
    name: str
    level: int
    current_exp: int
    gold: int
    battles_fought: int
    team: List[str]
    elementals: List[str]
    location: int
