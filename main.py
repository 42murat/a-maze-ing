#!/usr/bin/env python3
from mazeGeneration import generate_empty_maze
from temporaryMazeVisualization import show_maze

def main() -> None:
    print("Hellow Maze")
    maze = generate_empty_maze(
        width=8,
        height=7,
        x_start=2,
        y_start=1,
        x_end=6,
        y_end=6
    )
    show_maze(maze)

if __name__ == "__main__":
    main()
