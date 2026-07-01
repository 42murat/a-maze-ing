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
    maze_parameters = check_arguments(argv)
    maze = Maze(maze_parameters)
    maze.generate()
    export_to_file(maze)
    if (maze_parameters.visualize):
        visualize(maze)
    shortest_path = maze.get_shortest_path()
    print(shortest_path)

if __name__ == "__main__":
    main(sys.argv)