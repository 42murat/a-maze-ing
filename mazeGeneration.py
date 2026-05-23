"""
by: Jozef Bugajewski <jozefBugajewski@gmail.com>

This file contains and will contain class and it's fucntions that are related to maze generation,
for now I focus on trying to gererate solution-path in empty maze.
"""

# print("\u2610")  # ☐
# print("\u2611")  # ☑
# print("\u2612")  # ☒

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
        self.GREEN = "\033[32m"
        self.RED = "\033[31m"
        self.RESET = "\033[0m"

        self.width: int = width
        self.height: int = height
        self.x_start: int = x_start
        self.y_start: int = y_start
        self.x_end: int = x_end
        self.y_end: int = y_end
        self.maze: list[list[str]] = []

    def generate_empty(self) -> None:
        """Generates grid of squares in size defined by height and width. Shows input and output."""
        self.maze = [["☐" for _ in range(self.width)] for _ in range(self.height)]
        self.maze[self.y_start][self.x_start] = self.GREEN + self.maze[self.y_start][self.x_start] + self.RESET
        self.maze[self.y_end][self.x_end] = self.RED + self.maze[self.y_end][self.x_end] + self.RESET

