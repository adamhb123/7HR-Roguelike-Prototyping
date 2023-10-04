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
    def collides(self, rect: "Rect" | List["Rect"]) -> bool | List[bool]:
        if type(rect) == list:
            return any([self.collides(r) for r in rect])
        return (
            self.x < rect.x + rect.w
            and self.x + self.w > rect.x
            and self.y < rect.y + rect.h
            and self.y + self.h > rect.y
        )
    
class Tile(Enum):
    FLOOR=0
    FILL=1
    WALL_HOR=2
    WALL_VERT=3
    ENEMY=4
    KEY=5
    GOLD=6
    PLAYER=7

class Map:
    def __init__(self, w: int, h: int):
        self.w = w
        self.h = h
        self.rooms: List[Rect] = []
        self.reset_state()
        self._place_room_randomly()

    def reset_state(self):
        self.state = [[Tile.FILL.value for x in range(0, self.w)] for y in range(0, self.h)]

    def _update_rooms(self):
        for room in self.rooms:
            # Place horizontal walls
            print(self.state)
            for x in range(room.x, room.x + room.w):
                self.state[room.y][x] = Tile.WALL_HOR.value
                self.state[room.y+room.h][x] = Tile.WALL_HOR.value
            # Place vertical walls
            for y in range(room.y, room.y+room.h):
                self.state[y][room.x] = Tile.WALL_VERT.value
                self.state[y][room.x+room.w] = Tile.WALL_VERT.value
            # Carve inside
            for y in range(room.y+1, room.y+room.h-1):
                for x in range(room.x+1, room.x+room.w-1):
                    self.state[y][x] = Tile.FLOOR.value

    def _place_room_randomly(self, w: int=5, h: int=5):
        new_room = Rect(random.randint(0, self.w-w), random.randint(0, self.h-h), w, h)
        print(new_room)
        if self.rooms and new_room.collides(self.rooms):
            return False
        self.rooms.append(new_room)
        self._update_rooms()
        return True
    
    def get_tile_at(self, x: int, y: int):
        return self.state[y][x]
    
    def generate_rooms(self, n_attempts: int, width_range: Tuple[int, int], height_range: Tuple[int, int]):
        for _ in range(0, n_attempts):
            try:
                self._place_room_randomly(random.randint(width_range[0], width_range[1]),
                             random.randint(height_range[0], height_range[1]))
            except Exception as e:
                print(e)

    #def generate_maze(self, max_room_attempts:):
     #   x,y = 0,0
      #  while 
        

