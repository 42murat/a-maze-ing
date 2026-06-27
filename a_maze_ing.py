#!/usr/bin/env python3
import sys
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

    def render_cell_row(row: list[str]) -> str:
        """Renders the cell interiors and vertical boundaries for a maze row."""
        row_segments: list[str] = []
        for index, cell in enumerate(row):
            has_north_wall, has_east_wall, has_south_wall, has_west_wall = get_cell_walls(cell)
            if index == 0:
                row_segments.append("|" if has_west_wall else " ")
            row_segments.append("   ")
            row_segments.append("|" if has_east_wall else " ")
        return "".join(row_segments)

    def temp_visualize(maze: Maze) -> None:
        print("Maze:")
        maze_hex = maze.get_maze_hex()
        for row_index, row in enumerate(maze_hex):
            if row_index == 0:
                print(render_wall_row(row, 0))
            print(render_cell_row(row))
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
    a = 1
    print(maze.get_shortest_path())

if __name__ == "__main__":
    main(sys.argv)