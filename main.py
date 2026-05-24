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
        width=20,
        height=20,
        x_start=19,
        y_start=1,
        x_end=0,
        y_end=0
    )
    maze.generate_empty()
    show_maze(maze)
    t.sleep(1)

    max_steps = 500
    steps = 0
    for i in range(max_steps):
        if i < max_steps / 4:
            maze.generate_path_step(-0.05)
        elif i < max_steps / 2:
            maze.generate_path_step(0)
        else:
            maze.generate_path_step(0.3)
        steps += 1
        clear()
        show_maze(maze)
        t.sleep(0.01)
        if maze.x_current == maze.x_end and maze.y_current == maze.y_end:
            break
    if maze.x_current == maze.x_end and maze.y_current == maze.y_end:
        print("Find exit in:", steps, "steps.")
    else:
        print("Cannot find exit in:", steps, "steps.")

if __name__ == "__main__":
    main()
