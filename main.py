#!/usr/bin/env python3
from mazeGeneration import Maze
from temporaryMazeVisualization import show_maze
import time as t
import os

#Test
import subprocess
import sys
import os

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

    #VIBE CODING
    #THATS EVEN MORE EXPERIMENTAL FEATURE
    maze_width = 50
    maze_height = 50
    if os.environ.get("IN_NEW_WINDOW") != "1":
        env = os.environ.copy()
        env["IN_NEW_WINDOW"] = "1"

        subprocess.Popen([
            "gnome-terminal",
            f"--geometry={maze_width * 2}x{maze_height + 2}",
            "--",
            "bash",
            "-c",
            f"IN_NEW_WINDOW=1 python3 {sys.argv[0]}; read -n 1 -s -p ''"
        ])

        sys.exit()
    clear()
    maze = Maze(
        width=maze_width,
        height=maze_height,
        x_start=9,
        y_start=1,
        x_end=49,
        y_end=49
    )
    maze.generate_empty()
    show_maze(maze)
    t.sleep(1)

    max_steps = 2500
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
        t.sleep(0.03)
        if maze.x_current == maze.x_end and maze.y_current == maze.y_end:
            break
    if maze.x_current == maze.x_end and maze.y_current == maze.y_end:
        print("Find exit in:", steps, "steps.")
    else:
        print("Cannot find exit in:", steps, "steps.")

if __name__ == "__main__":
    main()
