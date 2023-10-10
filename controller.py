from typing import Tuple
from engine import Map, Tile, Event
from entities import Player


class Controller:
    def __init__(self, map: Map, player: Player):
        self._map = map
        self._player = player

    def _check_valid_move(self, start_pos: Tuple[int, int], direction: int):
        print(self._map.get_tile_at(start_pos[0], start_pos[1]-1))
        # Movement checks
        if direction == 0: # UP
            to = (start_pos[0], start_pos[1]-1)
            tile = self._map.get_tile_at(to[0], to[1])
        elif direction == 1: # RIGHT
            to = (start_pos[0]+1, start_pos[1])
            tile = self._map.get_tile_at(to[0], to[1])
        elif direction == 2: # DOWN
            to = (start_pos[0], start_pos[1]+1)
            tile = self._map.get_tile_at(to[0], to[1])
        elif direction == 3: # LEFT
            to = (start_pos[0]-1, start_pos[1])
            tile = self._map.get_tile_at(to[0], to[1])

        if tile == Tile.EMPTY.value:
            event = Event.STEP
        elif tile == Tile.ENEMY.value:
            event = Event.BATTLE
        elif tile == Tile.GOLD.value or tile == Tile.KEY.value:
            event = Event.PICKUP
        else: # Wall hit
            event = Event.NULL
            to = (start_pos[0], start_pos[1]) # If we hit a wall, move nowhere
        return event, tile, start_pos, to
        
    def handle_input(self, key: str):
        player_pos = self._map._find_entities(Tile.PLAYER)[0]
        if "KEY_UP" in key:
            event, to_tile, to = self._check_valid_move(player_pos, 0)
        elif "KEY_RIGHT" in key:
            event, to_tile, to = self._check_valid_move(player_pos, 1)
        elif "KEY_DOWN" in key:
            event, to_tile, to = self._check_valid_move(player_pos, 2)
        elif "KEY_LEFT" in key:
            event, to_tile, to = self._check_valid_move(player_pos, 3)
        return event, to_tile, to
        