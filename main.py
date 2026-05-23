#!/usr/bin/env python3
from mazeGeneration import Maze
from temporaryMazeVisualization import show_maze
import time as t
import os

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def main() -> None:
    clear()
    maze = Maze(
        width=8,
        height=7,
        x_start=2,
        y_start=1,
        x_end=6,
        y_end=6
    )
    maze.generate_empty()
    show_maze(maze)
    t.sleep(1)

    steps = 100
    for _ in range(steps):
        maze.generate_path_step()
        clear()
        #print(maze.x_current)
        #print(maze.y_current)
        show_maze(maze)
        t.sleep(0.4)

if __name__ == "__main__":
    main()
