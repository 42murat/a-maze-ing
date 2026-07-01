
from __future__ import annotations

import random
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .maze import Maze


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
                        cell = self.maze.Cell(x, y, cell_sub_maze_id)
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

            def _available_walls(self, cell: Maze.Cell, perfect_maze: bool = True) -> list[str]:
                        """Returns list of walls that can be removed from cell.
                        
                        If perfect_maze is True the function will return only
                        walls that can be removed without creating loops in maze. 
                        If perfect_maze is False the function will return all 
                        walls that can be removed from cell."""
                        walls: list[str] = []
                        top_cell = self.maze.get_N_cell(cell)
                        right_cell = self.maze.get_E_cell(cell)
                        bottom_cell = self.maze.get_S_cell(cell)
                        left_cell = self.maze.get_W_cell(cell)
                        if (
                            top_cell
                            and cell.N_wall
                            and top_cell.sub_maze_id != -1
                            and (cell.sub_maze_id != top_cell.sub_maze_id
                                 or not perfect_maze)
                        ):
                            walls.append("N")
                        if (
                            right_cell
                            and cell.E_wall
                            and right_cell.sub_maze_id != -1
                            and (cell.sub_maze_id != right_cell.sub_maze_id
                                 or not perfect_maze)
                        ):
                            walls.append("E")
                        if (
                            bottom_cell
                            and cell.S_wall
                            and bottom_cell.sub_maze_id != -1
                            and (cell.sub_maze_id != bottom_cell.sub_maze_id
                                 or not perfect_maze)
                        ):
                            walls.append("S")
                        if (
                            left_cell
                            and cell.W_wall
                            and left_cell.sub_maze_id != -1
                            and (cell.sub_maze_id != left_cell.sub_maze_id
                                 or not perfect_maze)
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
                else:
                    while len(self.cells_by_id) > 1:
                        self._try_remove_random_wall()

            def remove_wall(self, cell : Maze.Cell, wall: str) -> None:
                """Removes wall connecting cell and cell in a direction
                of wall. Does not check wheter such move makes maze
                not validates its conditions."""
                if wall == "N":
                    cell.N_wall = False
                    top_cell = self.maze.get_N_cell(cell)
                    top_cell.S_wall = False
                elif wall == "E":
                    cell.E_wall = False
                    right_cell = self.maze.get_E_cell(cell)
                    right_cell.W_wall = False
                elif wall == "S":
                    cell.S_wall = False
                    bottom_cell = self.maze.get_S_cell(cell)
                    bottom_cell.N_wall = False
                elif wall == "W":
                    cell.W_wall = False
                    left_cell = self.maze.get_W_cell(cell)
                    left_cell.E_wall = False

            def restore_wall(self, cell: Maze.Cell, wall: str) -> None:
                """Restores wall connecting cell and cell in a direction
                of wall. Does not check wheter such move makes maze
                not validates its conditions."""
                if wall == "N":
                    cell.N_wall = True
                    top_cell = self.maze.get_N_cell(cell)
                    top_cell.S_wall = True
                elif wall == "E":
                    cell.E_wall = True
                    right_cell = self.maze.get_E_cell(cell)
                    right_cell.W_wall = True
                elif wall == "S":
                    cell.S_wall = True
                    bottom_cell = self.maze.get_S_cell(cell)
                    bottom_cell.N_wall = True
                elif wall == "W":
                    cell.W_wall = True
                    left_cell = self.maze.get_W_cell(cell)
                    left_cell.E_wall = True

            def open_3x3_box(self, x_center: int, y_center: int) -> bool:
                """Checks if a 3x3 area around the given center point is completely open.
                If the center cell is on the edge of the maze it assumes that the cells
                outside the maze are closed (not open), so it wont omit condition."""
                center_cell = self.maze.get_cell(x_center, y_center)
                if not center_cell:
                    return False
                top_cell = self.maze.get_N_cell(center_cell)
                right_cell = self.maze.get_E_cell(center_cell)
                bottom_cell = self.maze.get_S_cell(center_cell)
                left_cell = self.maze.get_W_cell(center_cell)
                if not top_cell or not right_cell or not bottom_cell or not left_cell:
                    return False
                if any(
                    [len(center_cell.get_walls()),
                    top_cell.E_wall,
                    top_cell.W_wall,
                    right_cell.N_wall,
                    right_cell.S_wall,
                    bottom_cell.E_wall,
                    bottom_cell.W_wall,
                    left_cell.N_wall,
                    left_cell.S_wall]
                ):
                    return False
                return True


            def maze_too_open_arround(self, cell: Maze.Cell, wall: str) -> bool:
                """Checks whether removing wall from cell would make maze too open.
                
                The maze can't have large open areas. Corridors can't be wider
                than 2 cells. For example, you can have 2x3 or 3x2 open area,
                but never a 3x3 open area."""
                if wall == "N" or wall == "S":
                    x_filter = [cell.x - 1, cell.x, cell.x + 1]
                    if wall == "N" :
                        y_filter = [cell.y, cell.y + 1] 
                    else:
                        y_filter = [cell.y - 1, cell.y]
                elif wall == "E" or wall == "W":
                    if wall == "E":
                        x_filter = [cell.x, cell.x + 1]
                    else:
                        x_filter = [cell.x - 1, cell.x]
                    y_filter = [cell.y - 1, cell.y, cell.y + 1]
                result = False
                for y in y_filter:
                    for x in x_filter:
                        if self.open_3x3_box(x, y):
                            result = True
                return result

            def try_remove_wall(self, cell: Maze.Cell, wall: str) -> bool:
                """Tryies to remove wall. If success return true.
                Fails if by remoing wall the maze would become too open.
                """
                self.remove_wall(cell, wall)
                if self.maze_too_open_arround(cell, wall):
                    self.restore_wall(cell, wall)
                    return False
                return True

            def remove_some_walls(self) -> None:
                """Removes some walls from maze to create loops in maze, it ensures
                that there would be at least more than one solution path in maze.
                #FIXME: For now it doesnt
                
                This is take into account condition:
                    The maze can't have large open areas. Corridors can't be wider
                    than 2 cells. For example, you can have 2x3 or 3x2 open area,
                    but never a 3x3 open area."""
                self.available_cells.clear()
                ids = list(self.cells_by_id.keys())
                id = ids[0] if ids[0] != -1 else ids[1]
                self.available_cells = self.cells_by_id[id]
                removed_walls = 0
                while removed_walls < 120000 and len(self.available_cells) > 0:
                    cell = self.rng.choice(self.available_cells)
                    available_walls = self._available_walls(cell, perfect_maze=False)
                    if len(available_walls) == 0:
                        self.available_cells.remove(cell)
                        continue
                    for wall in available_walls:
                        if self.try_remove_wall(cell, wall):
                            removed_walls += 1
                            continue
                    self.available_cells.remove(cell)
                         
                    
