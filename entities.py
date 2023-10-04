from dataclasses import dataclass
import random
from typing import Tuple


@dataclass
class CharacterEntity:
    health: int
    strength: int
    def attack(self, other: 'CharacterEntity'):
        other.health -= self.strength
    
@dataclass
class Player(CharacterEntity):
    keys: int = 0
    gold: int = 0

@dataclass
class Enemy(CharacterEntity):
    gold_drop_range: Tuple[int] # Gold drops
    def drop(self):
        return random.randint(self.gold_drop_range[0], self.gold_drop_range[1])
    