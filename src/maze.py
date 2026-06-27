from __future__ import annotations
from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .maze_generator import MazeGenerator

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
                 width: int = 19,
                 height: int = 19,
                 entry_x: int = 0,
                 entry_y: int = 0,
                 exit_x: int = 1,
                 exit_y: int = 0,
                 output_file_path: str = "output_maze.txt",
                 perfect: bool = True,
                 visualize: bool = True,
                 seed: int = 42
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
        self.seed: int = seed

class Maze:
    def __init__(self, parameters: MazeParameters):
        """Initialize maze object - it's content (cells) is not initialized yet."""
        from .maze_generator import MazeGenerator

        self.parameters: MazeParameters = parameters
        self.cells: list[list[Maze.Cell]] = []
        self.generator: MazeGenerator = MazeGenerator(self)
    
    

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
    
    def get_N_cell(self, cell: Cell) -> Cell | None:
        """Returns maze cell at coordinates (x, y + 1) or None if cell is on maze border."""
        if cell.y == self.parameters.height - 1:
            return None
        return self.get_cell(cell.x, cell.y + 1)
    
    def get_E_cell(self, cell: Cell) -> Cell | None:
        """Returns maze cell at coordinates (x + 1, y) or None if cell is on maze border."""
        if cell.x == self.parameters.width - 1:
            return None
        return self.get_cell(cell.x + 1, cell.y)
    
    def get_S_cell(self, cell: Cell) -> Cell | None:
        """Returns maze cell at coordinates (x, y - 1) or None if cell is on maze border."""
        if cell.y == 0:
            return None
        return self.get_cell(cell.x, cell.y - 1)
    
    def get_W_cell(self, cell: Cell) -> Cell | None:
        """Returns maze cell at coordinates (x - 1, y) or None if cell is on maze border."""
        if cell.x == 0:
            return None
        return self.get_cell(cell.x - 1, cell.y)

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

