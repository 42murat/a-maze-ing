"""
by: Jozef Bugajewski <jozefBugajewski@gmail.com>

Here I just tested if I can use random with seed and it worked perfectly fine.
"""
from __future__ import annotations

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from mazeGeneration import Maze
import random
from const import N, E, S, W


rng = random.Random(42)

def get_random_direction() -> int:
    """Returns random direction, representation of: {N, E, S, W}
    """
    number = rng.randint(1,4)
    if number == 1:
        return N
    elif number == 2:
        return E
    elif number == 3:
        return S
    elif number == 4:
        return W
    else:
        return 67
    
def get_direction(maze: Maze, p: float = 0.1):
    """Returns direction for path generation.
    
    The direction probability is corelated (for now its constant diffrence) to how
    much the output coorditates are diffriend form current.
    The 'p' factor influence how much output direction is prefered
        p shoud be in range <0.00, 1.00> with step 0.01, 
        1.00 means that direction cant point away form exit (except it can go side ways:
            lets say x diff is 0 and y is -10, so direction cant be N but can be E or W
            even it E and W will point away form 'optimal' path it is health for maze 
            randomness)
        0.00 means there is no direction preferation and fucntion just performs 'random walk'"""
    def sign(x):
        return 1 if x > 0 else -1 if x < 0 else 0

    x_diff = maze.x_end - maze.x_current
    y_diff = maze.y_end - maze.y_current
    array_size = 4000
    probability_array = []
    for _ in range((int)((array_size / 4) * (1 + p * sign(y_diff)))):
        probability_array.append(N)
    for _ in range((int)((array_size / 4) * (1 - p * sign(y_diff)))):
        probability_array.append(S)
    for _ in range((int)((array_size / 4) * (1 + p * sign(x_diff)))):
        probability_array.append(E)
    for _ in range((int)((array_size / 4) * (1 - p * sign(x_diff)))):
        probability_array.append(W)
    #print("dummy")
    number = rng.randint(0,array_size - 1)
    return probability_array[number]