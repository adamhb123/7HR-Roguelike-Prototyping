

import math
import time
from typing import Tuple

def distance(a: Tuple[int, int], b: Tuple[int, int]):
    return math.sqrt((b[0]-a[0])**2 + (b[1]-b[1])**2)

def shortest_path(a: Tuple[int, int], b: Tuple[int, int]):
    possible_directions = (1 if a[0] < b[0] else -1, 1 if a[1] < b[1] else -1)
    print(possible_directions)
    path = [a]
    while path[-1] != b:
        # Take a step in both possible directions:
        step_hor = (path[-1][0] + possible_directions[0], path[-1][1])
        step_vert = (path[-1][0], path[-1][1] + possible_directions[1])
        d_h, d_v = distance(step_hor, b), distance(step_vert, b)
        # Get minimum distance between steps and b, this is inherently preferential to vertical steps
        best_step = step_hor if d_h < d_v else step_vert
        #print(f"path[-1]={path[-1]} d_h={d_h} d_v={d_v}")
        path.append(best_step)
        #time.sleep(.25)
    return path
