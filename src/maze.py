from __future__ import annotations
from dataclasses import dataclass

@dataclass
class MazeParameters:
    """Probably will contain all config file values, like.
    
    Exampler structure will be:
    def __init(self, argv: list[str]):
        <some input split>
        ...
        self.visualize: bool = visualize
        ..."""
    #FIXME: For now I'm mocking arguments, because other functions depends on it.
    def __init__(self,
                 width: int = 10,
                 height: int = 10,
                 entry_x: int = 0,
                 entry_y: int = 0,
                 exit_x: int = 9,
                 exit_y: int = 9,
                 output_file_path: str = "output_maze.txt",
                 perfect: bool = True,
                 visualize: bool = True
                ):
        self.width: int = width
        self.height: int = height
        self.entry_x: int = entry_x
        self.entry_y: int = entry_y
        self.exit_x: int = exit_x
        self.exit_y: int = exit_y
        self.output_file_path: str = output_file_path
        self.perfect: bool = perfect
        self.visualize: bool = visualize

class Maze:
    def __init__(self, parameters: MazeParameters):
        """Initialize maze object - it's content (cells) is not initialized yet."""
        self.parameters: MazeParameters = parameters
        self.cells: list[list[Maze.Cell]] = []
        self.generator: Maze.MazeGenerator = Maze.MazeGenerator(self)
    
    class MazeGenerator:
            def __init__(self, maze: Maze):
                self.maze: Maze = maze
                self.cells_by_id: dict[int, list[Maze.Cell]] = {}

            def fill_all_cells(self) -> None:
                """Set all maze cells to fully closed (all walls occupied)."""
                cell_sub_maze_id: int = 0
                for y in range(self.maze.parameters.height):
                    row: list[Maze.Cell] = []
                    for x in range(self.maze.parameters.width):
                        cell = Maze.Cell(x, y, cell_sub_maze_id)
                        row.append(cell)
                        self.cells_by_id.setdefault(cell_sub_maze_id, []).append(cell)
                        cell_sub_maze_id += 1
                    self.maze.cells.append(row)

            def set_42_pattern(self) -> None:
                """Set some maze cells sub_maze_id to value that prevents them form
                being part of maze during generation. 
                
                This is to satisfy condition:
                    The maze must contain a visible “42” drawn
                    by several fully closed cells.
                    
                For now I assume 42 will be drawm in 7x5 area, in the center of the maze.
                If maze height and width are odd values the patter in perfectly centered,
                if one of them is even the pattern is shifted by 1 cell to the left or up.
                
                Because of that is gennerally better to avoid maze input and output to be
                whole ractangle and in region near it.
                
                If the 42 parrert is in conflict with maze entry or exit or maze size is too small
                the pattern will not be drawn in this maze."""
                pattern_42: list[list[int]] = [
                    [1, 0, 0, 0, 1, 1, 1],
                    [1, 0, 0, 0, 0, 0, 1],
                    [1, 1, 1, 0, 1, 1, 1],
                    [0, 0, 1, 0, 1, 0, 0],
                    [0, 0, 1, 0, 1, 1, 1]
                ]
                def check_entry_exit_in_42_pattern() -> bool:
                    """Checks whether maze entry or exit is in 42 pattern."""
                    for y, row in enumerate(reversed(pattern_42)):
                        for x, pattern in enumerate(row):
                            if pattern == 1:
                                if (
                                    (pattern_x_offset + x == (self.maze.parameters.entry_x or self.maze.parameters.exit_x))
                                    and (pattern_y_offset + y == (self.maze.parameters.entry_y or self.maze.parameters.exit_y))
                                ):
                                    return True
                    return False

                if self.maze.parameters.width < 9 or self.maze.parameters.height < 7:
                    print(
                        "Maze width must be at least 9 and height at least 7 to draw 42 pattern."
                        "The 42 pattern will not be drawn in this maze."
                    )
                    return
                pattern_x_offset: int = (self.maze.parameters.width - 7) // 2
                pattern_y_offset: int = (self.maze.parameters.height - 5 + 1) // 2
                #FIXME: For now to see change I make all cells open.
                
                if check_entry_exit_in_42_pattern():
                    print(
                        "Maze entry or exit is in 42 pattern area." \
                        "The 42 pattern will not be drawn in this maze."
                    )
                    return
                for y, row in enumerate(reversed(pattern_42)):
                    for x, pattern in enumerate(row):
                        if pattern == 1:
                            self.maze.get_cell(pattern_x_offset + x, pattern_y_offset + y).sub_maze_id = -1
                            # self.maze.get_cell(pattern_x_offset + x, pattern_y_offset + y).N_wall = False
                            # self.maze.get_cell(pattern_x_offset + x, pattern_y_offset + y).E_wall = False
                            # self.maze.get_cell(pattern_x_offset + x, pattern_y_offset + y).S_wall = False
                            # self.maze.get_cell(pattern_x_offset + x, pattern_y_offset + y).W_wall = False

            def generate_perfect_maze(self) -> None:
                """Generates perfect maze (maze with no loops). All cells (except)
                cells in 42 pattern are part of maze. There is only one path
                connecting maze start with maze exit."""
                ...

            def remove_some_walls(self) -> None:
                """Removes some walls from maze to create loops in maze.
                
                This is take into account condition:
                    The maze can't have large open areas. Corridors can't be wider
                    than 2 cells. For example, you can have 2x3 or 3x2 open area,
                    but never a 3x3 open area."""
                ...


    def generate(self) -> None:
        """Cretes maze - do all stuff we talked about, like creating sollution path,
        filling the rest of maze, etc. Returns Maze class object."""
        ...

        self.generator.fill_all_cells()
        self.generator.set_42_pattern()
        self.generator.generate_perfect_maze()
        if not self.parameters.perfect:
            self.generator.remove_some_walls()


    class Cell:
        """Maze cell, contains x, y coordinates and cell status (what walls are occupied).
        The sub_maze_id is used to identify which sub-maze this cell belongs to. 
        This is useful for generating perfect mazes."""
        ...
        def __init__(
                self,
                x: int,
                y: int,
                sub_maze_id: int,
                N_wall: bool = True,
                E_wall: bool = True,
                S_wall: bool = True,
                W_wall: bool = True
        ):
            self.x: int = x
            self.y: int = y
            self.sub_maze_id: int = sub_maze_id
            self.N_wall: bool = N_wall
            self.E_wall: bool = E_wall
            self.S_wall: bool = S_wall
            self.W_wall: bool = W_wall

        def get_status(self) -> str:
            """Returns cell walls status in hex (string)."""
            return hex(self.N_wall<<0 | self.E_wall<<1 | self.S_wall<<2 | self.W_wall<<3)[2:].upper()
        
    def get_cell(self, x: int, y: int) -> Cell:
        """Returns maze cell at coordinates (x, y)."""
        return self.cells[y][x]

    def get_maze_hex(self) -> list[list[str]]:
        """Returns list list of strings, the outer list repesents maze rows,
        the inner maze cells in single row. Inner value is string representing
        cell status (what walls are occupied) in hex (string).
        
        When displaying the  maze rows viev  is form top to bottom, and when
            dispalying maze cells in single row view is from left to right."""
        #FOR NOW IM MOCKING THIS FUNCTION BECAUSE OTHER FUNCTIONS DEPENDS ON IT.
        #In example-maze.jpg there is what this maze looks like
        #THIS WHAT THIS FUCNTION COULD RETURN:
        # return [
        #     ["B", "D", "5", "3", "B"],
        #     ["C", "1", "7", "A", "A"],
        #     ["D", "2", "9", "6", "A"],
        #     ["9", "2", "A", "9", "2"],
        #     ["E", "C", "4", "6", "E"]
        # ]
        result: list[list[str]] = []
        for row in reversed(self.cells):
            result_row: list[str] = []
            for cell in row:
                result_row.append(cell.get_status())
            result.append(result_row)
        return result

    def get_output_file_path(self) -> str:
        """Returns file path to which export maze."""
        ...

    def get_start_coord(self) -> str:
        """Returns coordinates of maze start."""
        #FOR NOW IM MOCKING THIS FUNCTION BECAUSE OTHER FUNCTIONS DEPENDS ON IT.
        #THIS WHAT THIS FUCNTION COULD RETURN:
        return "0,0"


    def get_end_coord(self) -> str:
        """Returns coordinates of maze exit."""
        #FOR NOW IM MOCKING THIS FUNCTION BECAUSE OTHER FUNCTIONS DEPENDS ON IT.
        #THIS WHAT THIS FUCNTION COULD RETURN:
        return "2,3"

    def get_shortest_path(self) -> str:
        """Returns shortes path connecting maze start with
        maze end. The return data is format like:
        SWNSWESESEEWS... and is string"""
        #FOR NOW IM MOCKING THIS FUNCTION BECAUSE OTHER FUNCTIONS DEPENDS ON IT.
        #THIS WHAT THIS FUCNTION COULD RETURN:
        return "NENNE"


    def re_generate(self) -> None:
        """Clears all maze cells and generate it's content once again."""
        def clear_maze(self) -> None:
            """clears maze cells"""
            ...
        self.clear_maze()
        self.generate()

