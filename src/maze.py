from __future__ import annotations
from dataclasses import dataclass
import random

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
        self.parameters: MazeParameters = parameters
        self.cells: list[list[Maze.Cell]] = []
        self.generator: Maze.MazeGenerator = Maze.MazeGenerator(self)
    
    class MazeGenerator:
            def __init__(self, maze: Maze):
                self.maze: Maze = maze
                self.cells_by_id: dict[int, list[Maze.Cell]] = {}
                self.available_cells: list[Maze.Cell] = []
                self.rng = random.Random(maze.parameters.seed)
                # self.removed_walls = 0

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
                            cell = self.maze.get_cell(pattern_x_offset + x, pattern_y_offset + y)
                            self.cells_by_id[cell.sub_maze_id].remove(cell)
                            if len(self.cells_by_id[cell.sub_maze_id]) == 0:
                                del self.cells_by_id[cell.sub_maze_id]
                            cell.sub_maze_id = -1
                            self.cells_by_id.setdefault(-1, []).append(cell)
                            # self.maze.get_cell(pattern_x_offset + x, pattern_y_offset + y).N_wall = False
                            # self.maze.get_cell(pattern_x_offset + x, pattern_y_offset + y).E_wall = False
                            # self.maze.get_cell(pattern_x_offset + x, pattern_y_offset + y).S_wall = False
                            # self.maze.get_cell(pattern_x_offset + x, pattern_y_offset + y).W_wall = False

            def _available_walls(self, cell: Maze.Cell) -> list[str]:
                        """Returns list of walls that can be removed from cell."""
                        walls: list[str] = []
                        top_cell = self.maze.get_N_cell(cell)
                        right_cell = self.maze.get_E_cell(cell)
                        bottom_cell = self.maze.get_S_cell(cell)
                        left_cell = self.maze.get_W_cell(cell)
                        if (
                            top_cell
                            and cell.N_wall
                            and top_cell.sub_maze_id != -1
                            and cell.sub_maze_id != top_cell.sub_maze_id
                        ):
                            walls.append("N")
                        if (
                            right_cell
                            and cell.E_wall
                            and right_cell.sub_maze_id != -1
                            and cell.sub_maze_id != right_cell.sub_maze_id
                        ):
                            walls.append("E")
                        if (
                            bottom_cell
                            and cell.S_wall
                            and bottom_cell.sub_maze_id != -1
                            and cell.sub_maze_id != bottom_cell.sub_maze_id
                        ):
                            walls.append("S")
                        if (
                            left_cell
                            and cell.W_wall
                            and left_cell.sub_maze_id != -1
                            and cell.sub_maze_id != left_cell.sub_maze_id
                        ):
                            walls.append("W")
                        return walls

            def _merge_sub_mazes(self, cell1: Maze.Cell, cell2: Maze.Cell) -> None:
                        """Merges two sub-mazes into one sub-maze. Updates all cells with 
                        this id in cells_by_id and available_cells_by_id.
                        
                        To make process more efficient the function always merges smaller
                        sub-maze into bigger sub-maze."""
                        if len(self.cells_by_id[cell1.sub_maze_id]) < len(self.cells_by_id[cell2.sub_maze_id]):
                            cell1, cell2 = cell2, cell1
                        sub_maze_id1 = cell1.sub_maze_id
                        sub_maze_id2 = cell2.sub_maze_id
                        # if sub_maze_id1 == sub_maze_id2:  #this might be useful in future, but for now I don't need it
                        #     return
                        for cell in self.cells_by_id[sub_maze_id2]:
                            cell.sub_maze_id = sub_maze_id1
                            self.cells_by_id[sub_maze_id1].append(cell)
                        del self.cells_by_id[sub_maze_id2]
                        # if sub_maze_id2 in self.available_cells_by_id:
                        #     del self.available_cells_by_id[sub_maze_id2]

            def _remove_random_wall(self, walls: list[str], cell: Maze.Cell) -> None:
                        """Removes random wall from cell and updates cells_by_id and available_cells_by_id."""
                        wall = self.rng.choice(walls)
                        # self.removed_walls += 1
                        if wall == "N":
                            cell.N_wall = False
                            top_cell = self.maze.get_N_cell(cell)
                            top_cell.S_wall = False
                            self._merge_sub_mazes(cell, top_cell)
                        elif wall == "E":
                            cell.E_wall = False
                            right_cell = self.maze.get_E_cell(cell)
                            right_cell.W_wall = False
                            self._merge_sub_mazes(cell, right_cell)
                        elif wall == "S":
                            cell.S_wall = False
                            bottom_cell = self.maze.get_S_cell(cell)
                            bottom_cell.N_wall = False
                            self._merge_sub_mazes(cell, bottom_cell)
                        elif wall == "W":
                            cell.W_wall = False
                            left_cell = self.maze.get_W_cell(cell)
                            left_cell.E_wall = False
                            self._merge_sub_mazes(cell, left_cell)

            def _nearby_cells_in_same_sub_maze(self, cell: Maze.Cell) -> int:
                """Returns number of cells in the same sub-maze that are nearby cell."""
                count: int = 0
                top_cell = self.maze.get_N_cell(cell)
                right_cell = self.maze.get_E_cell(cell)
                bottom_cell = self.maze.get_S_cell(cell)
                left_cell = self.maze.get_W_cell(cell)
                if top_cell and top_cell.sub_maze_id == cell.sub_maze_id:
                    count += 1
                if right_cell and right_cell.sub_maze_id == cell.sub_maze_id:
                    count += 1
                if bottom_cell and bottom_cell.sub_maze_id == cell.sub_maze_id:
                    count += 1
                if left_cell and left_cell.sub_maze_id == cell.sub_maze_id:
                    count += 1
                return count

            def _pick_semi_random_cell(self) -> Maze.Cell:
                """For fun to make maze look more like typical maze instead of just
                picking random cell form avaliable_cells I coded this algirithm,
                that preferce to pick cell that are in larger sub_mazes and at this
                sub_mazes ends - so the maze corridiors will be longer and there would
                be less splits in the maze."""
                import math as m
                keys = [x for x in self.cells_by_id if x != -1]
                weights = [
                    10 if len(self.cells_by_id[x]) == 1
                    else 10 if len(self.cells_by_id[x]) == 2
                    else 10 if len(self.cells_by_id[x]) == 3
                    else len(self.cells_by_id[x]) * 25
                    for x in keys
                        ]
                picked_sub_maze_id = self.rng.choices(
                    keys,
                    weights = weights,
                    k=1
                )[0]
                a = 1
                weights = [
                        1 if len(self._available_walls(cell)) == 3
                        or len(self._available_walls(cell)) == 4
                        else 100 if len(self._available_walls(cell)) == 2
                        else 1
                        for cell in self.cells_by_id[picked_sub_maze_id]
                    ]
                a = 1
                result = self.rng.choices(
                    self.cells_by_id[picked_sub_maze_id],
                    weights = weights,
                    k = 1
                )[0]
                return result


            def _try_remove_random_wall(self) -> None:
                    """Tryies to remove random wall from maze. 
                    If wall is removed the two sub-mazes are merged into one sub-maze. 
                    If wall can't be removed (because it part of maze side or 42 pattern or 
                    cells are already in the same sub-maze) the function does nothing.
                    
                    The function pick random cell from available_cells_by_id,
                    then pick random wall from this cell and try to remove it.
                    If wall is removed the two sub-mazes are merged into one sub-maze
                    and cells ids are updated in cells_by_id and available_cells_by_id."""
                    random_cell = self._pick_semi_random_cell()
                    # random_cell = self.rng.choice(self.available_cells)
                    available_walls = self._available_walls(random_cell)
                    if len(available_walls) == 0:
                        available_walls = self._available_walls(random_cell)
                        if random_cell in self.available_cells:
                            self.available_cells.remove(random_cell)
                        return
                    self._remove_random_wall(available_walls, random_cell)
                    if len(available_walls) <= 1:
                        self.available_cells.remove(random_cell)
                    a = 1
            
            def generate_perfect_maze(self) -> None:
                """Generates perfect maze (maze with no loops). All cells (except)
                cells in 42 pattern are part of maze. There is only one path
                connecting maze start with maze exit."""
                for row in self.maze.cells:
                    for cell in row:
                        if cell.sub_maze_id != -1:
                            self.available_cells.append(cell)
                if -1 in self.cells_by_id:
                    while len(self.cells_by_id) > 2:
                        self._try_remove_random_wall()
                    # a = 1
                else:
                    while len(self.cells_by_id) > 1:
                        self._try_remove_random_wall()

            def remove_some_walls(self) -> None:
                """Removes some walls from maze to create loops in maze
                
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

