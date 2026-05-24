"""
by: Jozef Bugajewski <jozefBugajewski@gmail.com>

This is functions that are used only during tests,
the finall visualization of project probably will be handle other way but this might be some entry point
"""
from __future__ import annotations

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from mazeGeneration import Maze
from ctypes import c_int8
from const import SQUARE_OCCUPIED_BIT

# print("\u2610")  # ☐
# print("\u2611")  # ☑
# print("\u2612")  # ☒

def show_maze(maze: Maze):
    """This function prints each row (and all it's cells) of maze in reverse order.
    
    Reason of reverse order is that when we create matrix the 0,0 point is on the top left,
    but in Cartasian coordinates this point is usually in left bottom so when printing first row becames last
    and last first and so on.
    Remember that this is only visual representation and does not change logic.
    The green cell represents maze input.
    The red cell represents maze output.
    """
    RESET = "\033[0m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"

    def format_cell(cell: c_int8, cell_x: int, cell_y: int) -> str:
        result = "☐"
        if cell_x == maze.x_start and cell_y == maze.y_start:
            result = GREEN + result + RESET
        elif cell_x == maze.x_end and cell_y == maze.y_end:
            result = RED + result + RESET
        elif cell_x == maze.x_current and cell_y == maze.y_current:
            result = "☒"
            result = YELLOW + result + RESET
        elif  cell >> SQUARE_OCCUPIED_BIT & 1 == 1:
            result = MAGENTA + result + RESET
        return result

    for y, row in enumerate(reversed(maze.maze)):
        print(" ".join(format_cell(cell, x ,maze.height - 1 - y) 
                       for x, cell in enumerate(row)))