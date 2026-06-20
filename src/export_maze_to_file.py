from src.maze import Maze

def to_file(content: str, file_path: str) -> None:
    """Helper function, it might be inside export_to_file insted,
    basically it just appears content(string) to specified file."""
    ...


def export_to_file(maze: Maze) -> None:
    """This function exports maze to file specified in config.txt,
    it's content should be probaby inside Maze class object."""
    maze_hex = maze.get_maze_hex()
    for row in maze_hex:
        for cell in row:
            to_file(cell, maze.get_output_file_path())
        to_file("\n", maze.get_output_file_path())
    
    to_file(maze.get_start_coord(), maze.get_output_file_path())
    to_file(maze.get_end_coord(), maze.get_output_file_path())
    to_file(maze.get_shortest_path(), maze.get_output_file_path())
    