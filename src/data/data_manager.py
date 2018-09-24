from typing import List

import boto3

from src.character.player import Player
from src.data.resources import ElementalResource, PlayerResource, ItemResource, InventoryResource
from src.elemental.elemental import Elemental
from src.elemental.elemental_factory import ElementalInitializer
from src.items.item_initializer import ItemInitializer


class DataManager:
    def __init__(self):
        dynamodb = boto3.resource('dynamodb')
        self.elemental_table = dynamodb.Table('Elementals')
        self.player_table = dynamodb.Table('Players')
        self.inventory_table = dynamodb.Table('Inventories')
        self.players = {}

    def get_player(self, user) -> Player or None:
        if user.id in self.players:
            return self.players[user.id]
        return self._fetch_player(user)

    def get_created_player(self, user) -> Player:
        """
        Create a Player profile for a Discord user if it doesn't exist, and then return it.
        """
        if user.id in self.players:
            return self.players[user.id]
        fetched = self._fetch_player(user)
        if fetched:
            return fetched
        return self._create_profile(user)

    def save_all(self, player: Player) -> None:
        self.update_player(player)
        self.update_inventory(player)
        self.update_team(player)

    def update_player(self, player: Player) -> None:
        self.player_table.put_item(Item=player.to_server())

    def update_inventory(self, player: Player) -> None:
        self.inventory_table.put_item(Item=player.inventory_to_server())

    def update_team(self, player: Player) -> None:
        with self.elemental_table.batch_writer() as batch:
            for elemental in player.team.elementals:
                batch.put_item(Item=elemental.to_server())

    def update_elemental(self, elemental: Elemental) -> None:
        self.elemental_table.put_item(Item=elemental.to_server())

    def _fetch_player(self, user) -> Player or None:
        response = self.player_table.get_item(Key={'id': user.id})
        try:
            resource = PlayerResource(**response['Item'])
            self.players[user.id] = Player.from_resource(resource)
            elementals = self._fetch_elementals(resource.elementals)
            self.players[user.id].set_elementals(elementals)
            team = self._get_team(resource.team, elementals)
            self.players[user.id].set_team(team)
            self._fetch_items(self.players[user.id])
            return self.players[user.id]
        except KeyError:
            return None

    def _fetch_items(self, player: Player) -> None:
        """
        Retrieves the player's items and adds them to the inventory.
        """
        response = self.inventory_table.get_item(Key={'id': player.id})
        try:
            inventory_resource = InventoryResource(**response['Item'])
            item_resources = [ItemResource(**item) for item in inventory_resource.items]
            for resource in item_resources:
                item = ItemInitializer.from_name(resource.name)
                player.add_item(item, resource.amount)
        except KeyError:
            pass

    @staticmethod
    def _get_team(ids: List[str], elementals: List[Elemental]) -> List[Elemental]:
        return [elemental for elemental in elementals if elemental.id in ids]

    def _fetch_elementals(self, ids: List[str]) -> List[Elemental]:
        elementals = []
        for id in ids:
            response = self.elemental_table.get_item(Key={'id': id})
            try:
                resource = response['Item']
                elemental = ElementalInitializer.from_server(
                    ElementalResource(**resource)
                )
                elementals.append(elemental)
            except KeyError:
                pass
        return elementals

    def _create_profile(self, user) -> Player:
        new_player = Player.from_user(user)
        new_player.add_starter_items()
        self.players[user.id] = new_player
        self.update_player(new_player)
        self.update_inventory(new_player)
        return new_player
