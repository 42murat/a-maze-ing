"""
by: Jozef Bugajewski <jozefBugajewski@gmail.com>

This file contains and will contain class and it's fucntions that are related to maze generation,
for now I focus on trying to gererate solution-path in empty maze.
"""
from ctypes import c_int8
from const import SQUARE_OCCUPIED_BIT

class Maze:
    def __init__(
            self,
            width: int = 10,
            height: int = 10,
            x_start: int = 4,
            y_start: int = 3,
            x_end: int = 8,
            y_end: int = 6
        ):
        """
        #FIXME: There is no check if argument are proper, like egz. if coordinates are inside maze or not
        x_start, x_end: should be in range (width - 1)
        y_start, y_end: should be in range (height - 1)
        """

        self.width: int = width
        self.height: int = height
        self.x_start: int = x_start
        self.y_start: int = y_start
        self.x_end: int = x_end
        self.y_end: int = y_end
        self.maze: list[list[c_int8]] = []

        #This values wont be prob in finall implementation - it is only for current path generation
        self.x_current: int = x_start
        self.y_current: int = y_start

    def generate_empty(self) -> None:
        """Generates grid of 0 in size defined by height and width. Shows input and output."""
        self.maze = [[0 for _ in range(self.width)] for _ in range(self.height)]
        self.maze[self.y_start][self.x_start] += 1 << SQUARE_OCCUPIED_BIT

