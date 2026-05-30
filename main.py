#!/usr/bin/env python3
from mazeGeneration import Maze
from temporaryMazeVisualization import show_maze
import time as t
import os

#Test

def clear():
    """Clear users console form text.
    
    It's usually executed before displaying maze."""
    os.system("cls" if os.name == "nt" else "clear")

def main() -> None:
    """For now generate empty maze. Then create solution-path step until finds exit or reach certain steps.


    The solution path is not valid - it can overlaps it self 
    (pass through some square more than once) and is random.
    Actually for test I make it have tendency to points away
    form maze exit at start,then after some steps is completly
    random,and after some steps it starts to points towards 
    exit - thats because I want it to be sligthly longer,
    but has to be discuss. 
    """
    clear()
    maze = Maze(
        width=35,
        height=35,
        x_start=24,
        y_start=1,
        x_end=0,
        y_end=9
    )
    maze.generate_empty()
    show_maze(maze)
    t.sleep(1)

    max_steps = 1500
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
        t.sleep(0.11)
        if maze.x_current == maze.x_end and maze.y_current == maze.y_end:
            break
    if maze.x_current == maze.x_end and maze.y_current == maze.y_end:
        print("Find exit in:", steps, "steps.")
    else:
        print("Cannot find exit in:", steps, "steps.")

if __name__ == "__main__":
    main()
