"""
by: Jozef Bugajewski <jozefBugajewski@gmail.com>

Here I just tested if I can use random with seed and it worked perfectly fine.
"""

import random

rng = random.Random(42)

def get_semi_random_int() -> int:
    """Return random int from 1 to 10 base on seed 42"""
    return rng.randint(1,10)