import math
import random
from dataclasses import dataclass
from enum import Enum
from typing import List, Optional, Tuple, Union
from entities import Entity, PlayerEntity
from utility import distance, shortest_path

@dataclass
class Position:
    x: int
    y: int
    def clone(self):
        return Position(self.x, self.y)
    def to_tuple(self):
        return self.x, self.y

@dataclass
class Size:
    w: int
    h: int

@dataclass
class Rect:
    """Rect object for representing rectangles by Position and Size.

    Used to represent rooms in the game.
    """
    position: Position
    size: Size
    def __repr__(self):
        return f"[RECT] x: {self.position.x} y: {self.position.y} w: {self.size.w} h: {self.size.h}"
    def collides(self, rect: "Rect" | List["Rect"], padding: int=1) -> bool | List[bool]:
        if type(rect) is list:
            return any([self.collides(r) for r in rect])
        return (
            self.position.x - padding < rect.position.x + rect.size.w
            and self.position.x + self.size.w + padding > rect.position.x
            and self.position.y - padding < rect.position.y + rect.size.h
            and self.position.y + self.size.h + padding > rect.position.y
        )
    
class Event(Enum):
    """Event Enum
    
    Describes an event in-game.
    """
    NULL=-1
    STEP=0
    BATTLE=1
    PICKUP=2

class TileType(Enum):
    """TileType Enum

    Describes a Tile object's "type" i.e. what it represents in-game.
    """
    EMPTY=0
    FILL=1
    WALL=2
    ENEMY=3
    KEY=4
    GOLD=5
    PLAYER=6
    @staticmethod
    def to_int(tile_type: 'TileType'):
        return tile_type.value

@dataclass
class Tile:
    """Tile object

    Used for representing tiles
    
    Instance Attributes:
        type (TileType) - Type of Tile
        entity (Optional[Entity]) - Optional Entity attribute, used as a container of any information relevant to the Tile. Defaults to None.
    """
    type: TileType
    entity: Optional[Entity]=None

EmptyTileSingleton = Tile(TileType.EMPTY)
FillTileSingleton = Tile(TileType.FILL)

class Map:
    def __init__(self, size: Size):
        self.size = size
        self.rooms: List[Rect] = []
        self._reset_state()
        

    def _reset_state(self):
        self.state = [[FillTileSingleton for x in range(0, self.size.w)] for y in range(0, self.size.h)]

    def reset(self):
        self._reset_state()
        self.generate_rooms(12, (2,5), (2,5))
        self.generate_corridors()

    def entities_step(self):
        entities = self._find_tiles(TileType.ENEMY)
        # Calculate shortest path for enemies, move them along path


    def handle_event(self, event: Event, tile: TileType, tile_pos: Position):
        if event == Event.BATTLE:
            pass
        elif event == Event.PICKUP:
            pass
    def time_step(self, player_pos: Position, to_tile: TileType | int, to: Position):
        self._map.move_entity(player_pos.x, player_pos.y, to.x, to.y)
        self.entities_step()

    def _update_rooms(self):
        for room in self.rooms:
            """# Place horizontal walls
            print(self.state)
            for x in range(room.x, room.x + room.w):
                self.state[room.y][x] = Tile.WALL.value
                self.state[room.y+room.h][x] = Tile.WALL.value
            # Place vertical walls
            for y in range(room.y, room.y+room.h):
                self.state[y][room.x] = Tile.WALL.value
                self.state[y][room.x+room.w] = Tile.WALL.value"""
            # Carve room
            for y in range(room.position.y, room.position.y+room.size.h):
                for x in range(room.position.x, room.position.x+room.size.w):
                    self.carve((x,y))

    def _place_room(self, position: Position, size: Size):
        new_room = Rect(position, size)
        if self.rooms and new_room.collides(self.rooms):
            #print(f"Can't place room: {new_room}")
            return False
        self.rooms.append(new_room)
        print(new_room)
        self._update_rooms()
        return True
    
    def _find_tiles(self, tile_type: TileType) -> List[Position]:
        locations: List[Position] = []
        for y in range(0,len(self.state)):
            for x in range(0,len(self.state[0])):
                if self.state[y][x].type == tile_type:
                    locations.append(Position(x,y))
        return locations

    
    def _place_entity(self, position: Position, entity_tile: Tile):
        if self.get_tile_at(position) == EmptyTileSingleton:
            self.state[position.y][position.x] = entity_tile
            return True
        return False

    def _place_entity_randomly(self, entity_tile: Tile, max_attempts: int = 10000):
        for _ in range(max_attempts):
            if self._place_entity(Position(random.randint(0,self.size.w), random.randint(0, self.size.h)), entity_tile):
                return True
        return False

    def _place_room_randomly(self, size: Size, outer_padding: int = 1):
        x = random.randint(outer_padding, self.size.w - size.w - outer_padding)
        y = random.randint(outer_padding, self.size.h - size.h - outer_padding)
        self._place_room(Position(x,y), size)
    
    def get_tile_at(self, position: Position):
        return self.state[position.y][position.x]
    
    def move_entity(self, from_position: Position, to_position: Position):
        self.state[to_position.y][to_position.x] = self.state[from_position.y][from_position.x]
        self.carve(from_position)

    def generate_rooms(self, n_attempts: int=100, width_range: Tuple[int, int]=(3,5), height_range: Tuple[int, int]=(3,5)):
        for _ in range(0, n_attempts):
            self._place_room_randomly(Size(random.randint(width_range[0], width_range[1]),
                            random.randint(height_range[0], height_range[1])))

    def carve(self, position: Union[Position, Tuple[int, int]]):
        x,y = (position.x,position.y) if type(position) == Position else position
        self.state[y][x] = EmptyTileSingleton
        
    def carve_many(self, positions: List[Position]):
        for position in positions:
            self.carve(position)

    def _state_as_position_tuples(self) -> List[Tuple[int, int]]:
        return [(x,y) for y in range(len(self.state)) for x in range(len(self.state[0]))]
    
    def path_exists(self, a: Position, b: Position):
        """Implement Dijkstra's algorithm to check if clear path from a to b exists in map

        Args:
            a (Tuple[int,int]): _description_
            b (Tuple[int, int]): _description_
        """
        def _get_neighbors(node: Tuple[int, int], node_set: List[Tuple]):
            return list(filter(lambda node: node in node_set, (
                    (node[0] + 1, node[1]), (node[0] - 1, node[1]),  # X
                    (node[0], node[1] + 1), (node[0], node[1] - 1), # Y
                    (node[0] - 1, node[1] - 1), (node[0] - 1, node[1] + 1), # Left corners
                    (node[0] + 1, node[1] - 1), (node[0] + 1, node[1] + 1)  # Right corners
            )))


        initial_node, goal_node = a.to_tuple(), b.to_tuple()
        unvisited_set = self._state_as_position_tuples()
        unvisited_set = map(lambda node: (node, math.inf if node is not initial_node else 0), unvisited_set) # Add distances
        current_node = initial_node
        # https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm
        unvisited_neighbors = _get_neighbors(current_node, unvisited_set)

    def generate_corridors(self, _debug_render_step_func=None):
        """Uses Euclidean distance to calculate the shortest path between each room, and carves paths from 
        each room to all others.
        """
        for i in range(len(self.rooms)):
            for j in range(i+1, len(self.rooms)):
                self.carve_many(shortest_path(self.rooms[i].position.to_tuple(), self.rooms[j].position.to_tuple()))
                if _debug_render_step_func:
                    _debug_render_step_func()
        
def initialize_game(size: Size=Size(72, 15), player: Optional[PlayerEntity] = None):
    map = Map(size)
    player = player if player else PlayerEntity(100,10)
    map._place_entity_randomly(Tile(TileType.PLAYER, player))
    return map, player

print(Map(Size(5,5))._state_as_positions())