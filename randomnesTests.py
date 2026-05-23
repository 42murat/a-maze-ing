"""
by: Jozef Bugajewski <jozefBugajewski@gmail.com>

Here I just tested if I can use random with seed and it worked perfectly fine.
"""

import random
from const import N, E, S, W

rng = random.Random(42)

def get_semi_random_int() -> int:
    """Return random int from 1 to 10 base on seed 42
    
    This is egzample fucntion"""
    return rng.randint(1,10)

def get_direction() -> int:
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