"""
by: Jozef Bugajewski <jozefBugajewski@gmail.com>

This file contains and will contain class and it's fucntions that are related to maze generation,
for now I focus on trying to gererate solution-path in empty maze.
"""
from ctypes import c_int8
from const import SQUARE_OCCUPIED_BIT, N, E, S, W
from mazeRandomnes import get_direction, get_random_direction

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

    def check_square_occupied(self, y: int, x: int) -> bool:
        if x < 0 or y < 0:
            raise IndexError
        if self.maze[y][x] & 1<<SQUARE_OCCUPIED_BIT == 1:
            return True
        else:
            return False


    def generate_empty(self) -> None:
        """Generates grid of 0 in size defined by height and width. Shows input and output."""
        self.maze = [[0 for _ in range(self.width)] for _ in range(self.height)]
        self.maze[self.y_current][self.x_current] += 1 << SQUARE_OCCUPIED_BIT

    def check_direction(self, direction: int) -> bool:
        """This fucntion checks if next step in the provided direction is valid.

        For now it only cares if square is in maze.
        """
        try:
            if direction == N:
                if self.y_current == self.height - 1 or self.check_square_occupied(self.y_current + 1, self.x_current):
                    return False
            if direction == E:
                if self.x_current == self.width - 1 or self.check_square_occupied(self.y_current, self.x_current + 1):
                    return False
            if direction == S:
                if self.y_current == 0 or self.check_square_occupied(self.y_current - 1, self.x_current):
                    return False
            if direction == W:
                if self.x_current == 0 or self.check_square_occupied(self.y_current, self.x_current - 1):
                    return False
        except IndexError:
            return False
        return True
    
    def check_is_dead_end(self, x: int = None, y: int = None) -> bool:
        """Checks if there is any not occupied square near current square, if not returns true, else false"""
        if x is None:
            x = self.x_current
        if y is None:
            y = self.y_current
        try:
            if not self.check_square_occupied(y + 1, x):
                return False
        except IndexError:
            pass
        try:
            if not self.check_square_occupied(y, x + 1):
                return False
        except IndexError:
            pass
        try:
            if not self.check_square_occupied(y - 1, x):
                return False
        except IndexError:
            pass
        try:
            if not self.check_square_occupied(y, x - 1):
                return False
        except IndexError:
            pass
        return True
    
    def change_current_square(self):
        """Replace current square to one form which you can create next step path."""
        from mazeRandomnes import rng
        while True:
            new_x = rng.randint(0, self.width - 1)
            new_y = rng.randint(0, self.height - 1)
            if self.check_square_occupied(new_y, new_x):
                if not self.check_is_dead_end(new_x, new_y):
                    self.x_current = new_x
                    self.y_current = new_y
                    return
    
    def update_possition(self, direction: int) -> None:
        """Change cell status (if it was current cell once it is accupied variable is set to true)."""
        if direction == N:
            self.y_current += 1
        if direction == E:
            self.x_current += 1
        if direction == S:
            self.y_current -= 1
        if direction == W:
            self.x_current -= 1
        self.maze[self.y_current][self.x_current] = self.maze[self.y_current][self.x_current] | 1 << SQUARE_OCCUPIED_BIT

    def generate_path_step(self, p: float) -> None:
        """Generate step for solution-path.
        
        Repeat this process untill step is valis (like not outside maze)."""
        direction = 0
        while True:
            direction = get_direction(self, p)
            if self.check_direction(direction):
                break
            else:
                if self.check_is_dead_end():
                    self.change_current_square()

        self.update_possition(direction)


