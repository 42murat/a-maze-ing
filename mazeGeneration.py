"""
by: Jozef Bugajewski <jozefBugajewski@gmail.com>

This file contains and will contain fucntions that are related to maze generation,
for now I focus on trying to gererate solution-path in empty maze.
"""

# print("\u2610")  # ☐
# print("\u2611")  # ☑
# print("\u2612")  # ☒

GREEN = "\033[32m"
RED = "\033[31m"
RESET = "\033[0m"


def generate_empty_maze(
        width: int = 10,
        height: int = 10,
        x_start: int = 4,
        y_start: int = 3,
        x_end: int = 8,
        y_end: int = 6
        ) -> list[list[str]]:
    """
    #FIXME: There is no check if argument are proper, like egz. if coordinates are inside maze or not
    x_start, x_end: should be in range (width - 1)
    y_start, y_end: should be in range (height - 1)
    """
    result = [["☐" for _ in range(width)] for _ in range(height)]
    result[y_start][x_start] = GREEN + result[y_start][x_start] + RESET
    result[y_end - 1][x_end] = RED + result[y_end][x_end] + RESET
    return result
