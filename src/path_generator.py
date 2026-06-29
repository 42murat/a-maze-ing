from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .maze import Maze


class PathGenerator:
    class Path:
        def __init__(self, start_cell: Maze.Cell):
            self.cells: list[Maze.Cell] = [start_cell]

    def __init__(self, maze: Maze):
        self.paths: list[PathGenerator.Path] = []
        self.maze: Maze = maze


    def are_cells_connected(self, cell1: Maze.Cell, cell2: Maze.Cell) -> bool:
        """Checks if two cells are connected (if there is no wall between them)."""
        if cell1.x == cell2.x and cell1.y == cell2.y + 1:
            return not cell1.S_wall and not cell2.N_wall
        elif cell1.x == cell2.x and cell1.y == cell2.y - 1:
            return not cell1.N_wall and not cell2.S_wall
        elif cell1.x == cell2.x + 1 and cell1.y == cell2.y:
            return not cell1.W_wall and not cell2.E_wall
        elif cell1.x == cell2.x - 1 and cell1.y == cell2.y:
            return not cell1.E_wall and not cell2.W_wall
        else:
            return False

    def get_reachable_cells(self, path: PathGenerator.Path) -> list[Maze.Cell]:
        """Returns list of cells that are reachable from the last cell in path."""
        result = []
        last_cell = path.cells[-1]
        top_cell = self.maze.get_N_cell(last_cell)
        right_cell = self.maze.get_E_cell(last_cell)
        bottom_cell = self.maze.get_S_cell(last_cell)
        left_cell = self.maze.get_W_cell(last_cell)
        if (
            top_cell
            and top_cell not in path.cells
            and self.are_cells_connected(last_cell, top_cell)
        ):
            result.append(top_cell)
        if right_cell and right_cell not in path.cells and self.are_cells_connected(last_cell, right_cell):
            result.append(right_cell)
        if bottom_cell and bottom_cell not in path.cells and self.are_cells_connected(last_cell, bottom_cell):
            result.append(bottom_cell)
        if left_cell and left_cell not in path.cells and self.are_cells_connected(last_cell, left_cell):
            result.append(left_cell)
        return result
    
    @staticmethod
    def decode_path(cells: list[Maze.Cell]) -> str:
        """Decodes a list of cells into a string of directions (N, E, S, W)."""
        directions = []
        for i in range(len(cells) - 1):
            current_cell = cells[i]
            next_cell = cells[i + 1]
            if next_cell.x == current_cell.x and next_cell.y == current_cell.y + 1:
                directions.append("N")
            elif next_cell.x == current_cell.x and next_cell.y == current_cell.y - 1:
                directions.append("S")
            elif next_cell.x == current_cell.x + 1 and next_cell.y == current_cell.y:
                directions.append("E")
            elif next_cell.x == current_cell.x - 1 and next_cell.y == current_cell.y:
                directions.append("W")
        return "".join(directions)

    def generate_solution_path(
            self,
            maze: Maze,
            start_cell: Maze.Cell,
            exit_cell: Maze.Cell
        ) -> str:
        """Looks for solution path (or shortest path to exit) that connects entry
        and exit cells."""
        self.paths.clear()
        path = self.Path(start_cell)
        self.paths.append(path)
        exit_not_found = True
        while exit_not_found:
            for path in self.paths[:]:
                # extra_paths = 0
                reachable_cells = self.get_reachable_cells(path)
                if len(reachable_cells) == 0:
                    self.paths.remove(path)
                elif len(reachable_cells) == 1:
                    path.cells.append(reachable_cells[0])
                    if reachable_cells[0] == exit_cell:
                        exit_not_found = False
                        return self.decode_path(path.cells)
                elif len(reachable_cells) > 1:
                    self.paths.remove(path)
                    for cell in reachable_cells:
                        new_path = self.Path(start_cell)
                        new_path.cells = path.cells.copy()
                        new_path.cells.append(cell)
                        self.paths.append(new_path)
                        if cell == exit_cell:
                            exit_not_found = False
                            return self.decode_path(self.paths[-1].cells)
                # for cell in reachable_cells:
                #     if extra_paths == 0:
                #         if cell not in path:
                #             path.cells.append(cell)
                #     else:
                #         new_path = path.copy()
                #         new_path.cells.append(cell)
                #         self.paths.append(new_path)
                #     if cell == exit_cell:
                #         exit_not_found = False
        return self.decode_path(self.paths[-1].cells)
        