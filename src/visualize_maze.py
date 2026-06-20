from src.maze import Maze

def visualize(maze : Maze) -> None:
    """Visualize maze inside condsole or using MLX.
    
    This function must handle user interactions (probably via some key-input),
    whether certain option is select, some action is needed.
    User interactions must be available, at least for the following tasks:
        • Re-generate a new maze and display it.
        • Show/Hide a valid shortest path from the entrance to the exit.
        • Change maze wall colours.
        • I think also quit option is needed.
    To get maze content get_maze_hex() return list[list[str]]:
        maze_hex = maze.get_maze_hex()
        for row in maze_hex:
            for cell in row:
                <cell is just string, has to be format and show on screen>
    The maze.re_generate() interface is provided to regenerate maze.
    Show hide shortest path must be visualize using this interface:
        -get_start_coord()
        -get_end_coord()
        -get_shortest_path()
    I think this function looks like:
    def show_maze(maze) -> None:
        maze_hex = maze.get_maze_hex()
        for row in maze_hex:
            for cell in row:
                show(cell) <- just covert string and put it screen
    show(maze)
    while True:
        action = get_user_input()
        if action == 1:
            maze.re_generate()
            show(maze)
        if action == 2:
            start = maze.get_start_coord()
            end = maze.get_end_coord()
            path = maze.get_shortest_path()
            show_hide_path(start, end, path)
        if action == 3:
            change_color()
        if action == 4:
            break;
    """
    ...