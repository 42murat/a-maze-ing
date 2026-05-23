"""
by: Jozef Bugajewski <jozefBugajewski@gmail.com>

This is functions that are used only during tests,
the finall visualization of project probably will be handle other way but this might be some entry point
"""
from mazeGeneration import Maze

def show_maze(maze: Maze):
    """This function prints each row (and all it's cells) of maze in reverse order.
    
    Reason of reverse order is that when we create matrix the 0,0 point is on the top left,
    but in Cartasian coordinates this point is usually in left bottom so when printing first row becames last
    and last first and so on.
    Remember that this is only visual representation and does not change logic.
    The green cell represents maze input.
    The red cell represents maze output.
    """
    for row in reversed(maze.maze):
        print(" ".join(cell for cell in row))