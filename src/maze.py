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
    

    def generate(self) -> None:
        """Cretes maze - do all stuff we talked about, like creating sollution path,
        filling the rest of maze, etc. Returns Maze class object."""
        ...
        class MazeGenerator:
            def __init__(self, maze: Maze):
                self.maze: Maze = maze

            def fill_all_cells(self) -> None:
                """Set all maze cells to fully closed (all walls occupied)."""
                ...

            def set_42_pattern(self) -> None:
                """Set some maze cells sub_maze_id to value that prevents them form
                being part of maze during generation. 
                
                This is to satisfy condition:
                    The maze must contain a visible “42” drawn
                    by several fully closed cells."""

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

        generator = MazeGenerator(self)

        generator.fill_all_cells()
        generator.set_42_pattern()
        generator.generate_perfect_maze()
        if not self.parameters.perfect:
            generator.remove_some_walls()


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

    def get_maze_hex(self) -> list[list[str]]:
        """Returns list list of strings, the outer list repesents maze rows,
        the inner maze cells in single row. Inner value is string representing
        cell status (what walls are occupied) in hex (string)."""
        #FOR NOW IM MOCKING THIS FUNCTION BECAUSE OTHER FUNCTIONS DEPENDS ON IT.
        #In example-maze.jpg there is what this maze looks like
        #THIS WHAT THIS FUCNTION COULD RETURN:
        return [
            ["B", "D", "5", "3", "B"],
            ["C", "1", "7", "A", "A"],
            ["D", "2", "9", "6", "A"],
            ["9", "2", "A", "9", "2"],
            ["E", "C", "4", "6", "E"]
        ]

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

