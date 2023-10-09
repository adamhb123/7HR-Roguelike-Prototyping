import random
from dataclasses import dataclass
from enum import Enum
from typing import List, Tuple

@dataclass
class Rect:
    x: int
    y: int
    w: int
    h: int
    def __repr__(self):
        return f"[RECT] x: {self.x} y: {self.y} w: {self.w} h: {self.h}"
    def collides(self, rect: "Rect" | List["Rect"], padding: int=1) -> bool | List[bool]:
        if type(rect) is list:
            return any([self.collides(r) for r in rect])
        return (
            self.x - padding < rect.x + rect.w
            and self.x + self.w + padding > rect.x
            and self.y - padding < rect.y + rect.h
            and self.y + self.h + padding > rect.y
        )
    
class Tile(Enum):
    EMPTY=0
    FILL=1
    WALL=2
    ENEMY=3
    KEY=4
    GOLD=5
    PLAYER=6

class Map:
    def __init__(self, w: int, h: int):
        self.w = w
        self.h = h
        self.rooms: List[Rect] = []
        self.reset_state()

    def reset_state(self):
        self.state = [[Tile.FILL.value for x in range(0, self.w)] for y in range(0, self.h)]

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
            for y in range(room.y, room.y+room.h):
                for x in range(room.x, room.x+room.w):
                    self.state[y][x] = Tile.EMPTY.value

    def _place_room(self, x: int, y: int, w: int=5, h: int=5):
        new_room = Rect(x, y, w, h)
        if self.rooms and new_room.collides(self.rooms):
            #print(f"Can't place room: {new_room}")
            return False
        self.rooms.append(new_room)
        print(new_room)
        self._update_rooms()
        return True
    
    def _place_entity(self, x: int, y: int, entity_tile: Tile | int):
        if self._get_tile_at(x, y) == Tile.EMPTY.value:
            self.state[y][x] = entity_tile.value if type(entity_tile) == Tile else entity_tile
            return True
        return False


    def _place_room_randomly(self, w: int=5, h: int=5, outer_padding: int = 1):
        x = random.randint(outer_padding, self.w - w - outer_padding)
        y = random.randint(outer_padding, self.h - h - outer_padding)
        self._place_room(x,y,w,h)
    
    def _get_tile_at(self, x: int, y: int):
        return self.state[y][x]
    
    def generate_rooms(self, n_attempts: int, width_range: Tuple[int, int], height_range: Tuple[int, int]):
        for _ in range(0, n_attempts):
            self._place_room_randomly(random.randint(width_range[0], width_range[1]),
                            random.randint(height_range[0], height_range[1]))

    def generate_corridors(self):
        

        
