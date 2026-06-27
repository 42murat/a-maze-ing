from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .maze import Maze


class PathGenerator:
    class Path:
        def __init__(self, start_cell: Maze.Cell):
            self.cells: list[Maze.Cell] = [start_cell]
            self.start_cell: Maze.Cell = start_cell
            self.end_cell: Maze.Cell = start_cell

    def __init__(self):
        self.paths: list[PathGenerator.Path] = []

    def generate_solution_path(
            self,
            maze: Maze,
            start_cell: Maze.Cell,
            exit_cell: Maze.Cell
        ) -> str:
        """Looks for solution path (or shortest path to exit) that connects entry
        and exit cells."""
        path = self.Path(start_cell)
        self.paths.append(path)
        exit_not_found = True
        while exit_not_found:
            for path in self.paths[:]:
                extra_paths = 0
                reachable_cells = maze.get_reachable_cells(path)
                for cell in reachable_cells:
                    if extra_paths == 0:
                        if cell not in path:
                            path.cells.append(cell)
                    else:
                        new_path = path.copy()
                        new_path.cells.append(cell)
                        self.paths.append(new_path)
                    if cell == exit_cell:
                        exit_not_found = False
        return ""
        