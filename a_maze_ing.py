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
    def print_cell(cell_hex: str) -> list[str]:
        """Converts a hex wall mask into a 3-line ASCII cell."""
        cell_status = int(cell_hex, 16)
        has_north_wall = bool(cell_status & 0x1)
        has_east_wall = bool(cell_status & 0x2)
        has_south_wall = bool(cell_status & 0x4)
        has_west_wall = bool(cell_status & 0x8)

        cell_width = 6
        inner_width = cell_width - 2

        top_line = " " + ("-" * inner_width if has_north_wall else " " * inner_width) + " "
        middle_line = (
            ("|" if has_west_wall else " ")
            + (" " * inner_width)
            + ("|" if has_east_wall else " ")
        )
        bottom_line = " " + ("-" * inner_width if has_south_wall else " " * inner_width) + " "
        return [top_line, middle_line, bottom_line]

    def temp_visualize(maze: Maze) -> None:
        print("Maze:")
        maze_hex = maze.get_maze_hex()
        for row in maze_hex:
            rendered_rows = ["", "", ""]
            for cell in row:
                cell_lines = print_cell(cell)
                for index, line in enumerate(cell_lines):
                    rendered_rows[index] += line
            for line in rendered_rows:
                print(line)

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

if __name__ == "__main__":
    main(sys.argv)