class MazeParameters:
    """Probably will contain all config file values, like.
    
    Exampler structure will be:
    def __init(self, argv: list[str]):
        <some input split>
        ...
        self.visualize: bool = visualize
        ..."""
    ...
    #FOR NOW TO MAKE OTHER PARTS PASS
    def __init__(self):
        self.visualize = True

class Maze:
    def __init__(self, parameters: MazeParameters):
        """Initialize maze object - it's content (cells) is not initialized yet."""
        self.parameters = parameters
    

    def generate(self) -> None:
        """Cretes maze - do all stuff we talked about, like creating sollution path,
        filling the rest of maze, etc. Returns Maze class object."""
        ...

    class cell:
        """Maze cell, contains x, y coordinates and cell status (what walls are occupied)"""
        ...
        def get_status() -> str:
            """Returns cell walls status in hex (string)."""

    def get_maze_hex(self) -> list[list[str]]:
        """Returns list list of strings, the outer list repesents maze rows,
        the inner maze cells in single row. Inner value is string representing
        cell status (what walls are occupied) in hex (string)."""
        #FOR NOW IM MOCKING THIS FUNCTION BECAUSE OTHER FUNCTIONS DEPENDS ON IT.
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

