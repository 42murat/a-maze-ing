#!/usr/bin/env python3
import sys
from unittest import result
from src.check_arguments import check_arguments
from src.export_maze_to_file import export_to_file
from src.visualize_maze import visualize
from src.maze import Maze


def main(argv: list[str]) -> None:
    """This is amazing main function
    
    I think <maze_parameters> should be some object of some class, that will
        hold out maze parameters.
    """
    def get_cell_walls(cell_hex: str) -> tuple[bool, bool, bool, bool]:
        """Converts a hex wall mask into directional wall flags."""
        cell_status = int(cell_hex, 16)
        has_north_wall = bool(cell_status & 0x1)
        has_east_wall = bool(cell_status & 0x2)
        has_south_wall = bool(cell_status & 0x4)
        has_west_wall = bool(cell_status & 0x8)
        return has_north_wall, has_east_wall, has_south_wall, has_west_wall

    def render_wall_row(row: list[str], wall_index: int) -> str:
        """Renders a horizontal boundary row using one wall per shared edge."""
        wall_segments = ["+"]
        for cell in row:
            cell_walls = get_cell_walls(cell)
            has_wall = cell_walls[wall_index]
            wall_segments.append(("---" if has_wall else "   ") + "+")
        return "".join(wall_segments)

    def build_solution_cells(maze: Maze, path: str) -> set[tuple[int, int]]:
        """Returns coordinates visited by the solution path, including start."""
        x = maze.parameters.entry_x
        y = maze.parameters.entry_y
        visited: set[tuple[int, int]] = {(x, y)}
        for direction in path:
            if direction == "N":
                y += 1
            elif direction == "E":
                x += 1
            elif direction == "S":
                y -= 1
            elif direction == "W":
                x -= 1
            visited.add((x, y))
        return visited

    def render_cell_row(
        row: list[str],
        row_y: int,
        solution_cells: set[tuple[int, int]],
        start: tuple[int, int],
        end: tuple[int, int],
    ) -> str:
        """Renders the cell interiors and vertical boundaries for a maze row."""
        row_segments: list[str] = []
        for index, cell in enumerate(row):
            has_north_wall, has_east_wall, has_south_wall, has_west_wall = get_cell_walls(cell)
            cell_x = index
            if (cell_x, row_y) == start:
                cell_text = " S "
            elif (cell_x, row_y) == end:
                cell_text = " E "
            elif (cell_x, row_y) in solution_cells:
                cell_text = " * "
            else:
                cell_text = "   "
            if index == 0:
                row_segments.append("|" if has_west_wall else " ")
            row_segments.append(cell_text)
            row_segments.append("|" if has_east_wall else " ")
        return "".join(row_segments)

    def temp_visualize(maze: Maze) -> None:
        print("Maze:")
        maze_hex = maze.get_maze_hex()
        path = maze.get_shortest_path()
        solution_cells = build_solution_cells(maze, path)
        start = (maze.parameters.entry_x, maze.parameters.entry_y)
        end = (maze.parameters.exit_x, maze.parameters.exit_y)
        for row_index, row in enumerate(maze_hex):
            row_y = maze.parameters.height - 1 - row_index
            if row_index == 0:
                print(render_wall_row(row, 0))
            print(render_cell_row(row, row_y, solution_cells, start, end))
            print(render_wall_row(row, 2))

    def temp_visualize_hex(maze: Maze) -> None:
        print("Maze hex:")
        maze_hex = maze.get_maze_hex()
        for row in maze_hex:
            for cell in row:
                print(cell, end=" ")
            print("")


    maze_parameters = check_arguments(argv)
    maze = Maze(maze_parameters)
    maze.generate()
    export_to_file(maze)
    if (maze_parameters.visualize):
        # visualize(maze)
        temp_visualize(maze)
        # temp_visualize_hex(maze)
    shortest_path = maze.get_shortest_path()
    print(shortest_path)

if __name__ == "__main__":
    main(sys.argv)