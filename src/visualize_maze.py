from src.maze import Maze
import os
import random


# ============================================================
# WALL BIT VALUES
# ============================================================
# Each maze cell is stored as a number.
#
# Example:
# 15 means all walls are closed.
#
# Binary idea:
# 1 = North wall
# 2 = East wall
# 4 = South wall
# 8 = West wall
#
# So if a cell has value 15:
# 15 = 1 + 2 + 4 + 8
# It means this cell has all 4 walls.
# ============================================================

NORTH = 1
EAST = 2
SOUTH = 4
WEST = 8


# ============================================================
# TERMINAL COLORS
# ============================================================
# These are ANSI background colors.
# They work in most terminals.
#
# We print two spaces "  " with a background color.
# This creates a square-like block in the terminal.
# ============================================================

RESET = "\033[0m"

BLACK_BG = "40"      # Empty space / corridor
WHITE_BG = "107"     # Maze walls
GRAY_BG = "47"       # Solution path
MAGENTA_BG = "45"    # Start / entry
RED_BG = "41"        # Exit

# Different wall colors for option 3
WALL_COLORS = [
    "107",   # bright white
    "46",    # cyan
    "42",    # green
    "44",    # blue
    "45",    # magenta
    "43",    # yellow
]


# ============================================================
# SMALL HELPER FUNCTIONS
# ============================================================

def clear_screen() -> None:
    """
    Clear the terminal screen.

    On Windows we use 'cls'.
    On Linux / macOS we use 'clear'.
    """
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


def print_block(background_color: str) -> str:
    """
    Return one colored block.

    We use two spaces because one terminal character is too narrow.
    Example:
        white background + two spaces = white wall block
    """
    return f"\033[{background_color}m  {RESET}"


def cell_to_number(cell) -> int:
    """
    Convert a maze cell to an integer.

    Sometimes cells can come as integers:
        15

    Sometimes cells can come as hexadecimal strings:
        "F"

    This function accepts both.
    """
    if isinstance(cell, int):
        return cell

    return int(str(cell).strip(), 16)


def has_wall(cell: int, wall: int) -> bool:
    """
    Check if a cell has a specific wall.

    Example:
        has_wall(15, NORTH) -> True
        has_wall(14, NORTH) -> False

    Because 14 does not contain the NORTH bit.
    """
    return bool(cell & wall)


def parse_coord(coord) -> tuple[int, int]:
    """
    Convert different coordinate formats into (x, y).

    This function accepts:

    1) Dictionary:
        {"x": 0, "y": 0}

    2) Tuple or list:
        (0, 0)
        [0, 0]

    3) String:
        "0,0"
    """
    if isinstance(coord, dict):
        return int(coord["x"]), int(coord["y"])

    if isinstance(coord, tuple) or isinstance(coord, list):
        return int(coord[0]), int(coord[1])

    x, y = str(coord).split(",")
    return int(x.strip()), int(y.strip())


# ============================================================
# READ DATA FROM MAZE OBJECT
# ============================================================
# We do not edit maze.py.
# Instead, we only read data from the maze object.
#
# This file supports two styles:
#
# 1) MazeGenerator style:
#       maze.grid
#       maze.entry
#       maze.exit
#       maze.solution_path
#
# 2) Your current Maze class style:
#       maze.get_maze_hex()
#       maze.get_start_coord()
#       maze.get_end_coord()
#       maze.get_shortest_path()
# ============================================================

def get_maze_grid(maze) -> list[list[int]]:
    """
    Get maze grid as list[list[int]].

    The visualizer needs numbers, not hex strings.
    So this function converts all cells to integers.
    """
    if hasattr(maze, "grid") and maze.grid:
        grid = []

        for row in maze.grid:
            new_row = []

            for cell in row:
                new_row.append(cell_to_number(cell))

            grid.append(new_row)

        return grid

    if hasattr(maze, "get_maze_hex"):
        maze_hex = maze.get_maze_hex()
        grid = []

        for row in maze_hex:
            new_row = []

            for cell in row:
                new_row.append(cell_to_number(cell))

            grid.append(new_row)

        return grid

    raise ValueError("Maze grid was not found.")


def get_start_position(maze) -> tuple[int, int]:
    """
    Get the maze entry/start position.
    """
    if hasattr(maze, "entry"):
        return parse_coord(maze.entry)

    if hasattr(maze, "get_start_coord"):
        return parse_coord(maze.get_start_coord())

    raise ValueError("Maze start position was not found.")


def get_exit_position(maze) -> tuple[int, int]:
    """
    Get the maze exit position.
    """
    if hasattr(maze, "exit"):
        return parse_coord(maze.exit)

    if hasattr(maze, "get_end_coord"):
        return parse_coord(maze.get_end_coord())

    raise ValueError("Maze exit position was not found.")


def get_solution_path(maze) -> str:
    """
    Get the solution path as a string.

    Example:
        "NENNE"

    It means:
        North
        East
        North
        North
        East
    """
    if hasattr(maze, "solution_path"):
        if isinstance(maze.solution_path, list):
            return "".join(maze.solution_path)

        return str(maze.solution_path)

    if hasattr(maze, "get_shortest_path"):
        return str(maze.get_shortest_path())

    return ""


# ============================================================
# PATH COORDINATE LOGIC
# ============================================================
# There are two possible coordinate systems:
#
# 1) Top-left system:
#       y grows downward
#       This is common in grids/lists.
#
# 2) Bottom-left system:
#       y grows upward
#       This is common in math coordinates.
#
# To avoid changing maze.py, this visualizer tries both systems
# and automatically chooses the one that reaches the exit.
# ============================================================

def move_with_top_left_system(
    x: int,
    y: int,
    move: str
) -> tuple[int, int]:
    """
    Move one step using top-left coordinate system.

    In this system:
        N means y - 1
        S means y + 1
    """
    if move == "N":
        y -= 1
    elif move == "S":
        y += 1
    elif move == "E":
        x += 1
    elif move == "W":
        x -= 1

    return x, y


def move_with_bottom_left_system(
    x: int,
    y: int,
    move: str
) -> tuple[int, int]:
    """
    Move one step using bottom-left coordinate system.

    In this system:
        N means y + 1
        S means y - 1
    """
    if move == "N":
        y += 1
    elif move == "S":
        y -= 1
    elif move == "E":
        x += 1
    elif move == "W":
        x -= 1

    return x, y


def build_path_cells(
    start: tuple[int, int],
    path: str,
    use_bottom_left_system: bool
) -> list[tuple[int, int]]:
    """
    Convert path string into real cell coordinates.

    Example:
        start = (0, 0)
        path = "NE"

    Result can be:
        [(0, 0), (0, 1), (1, 1)]
    """
    x, y = start
    path_cells = [(x, y)]

    for move in path:
        move = move.upper()

        if use_bottom_left_system:
            x, y = move_with_bottom_left_system(x, y, move)
        else:
            x, y = move_with_top_left_system(x, y, move)

        path_cells.append((x, y))

    return path_cells


def count_cells_inside_maze(
    path_cells: list[tuple[int, int]],
    width: int,
    height: int
) -> int:
    """
    Count how many path cells are inside the maze.

    This helps us choose the correct coordinate system.
    """
    count = 0

    for x, y in path_cells:
        if 0 <= x < width and 0 <= y < height:
            count += 1

    return count


def should_use_bottom_left_system(
    start: tuple[int, int],
    exit_position: tuple[int, int],
    path: str,
    width: int,
    height: int
) -> bool:
    """
    Try both coordinate systems.

    The better system is the one where:
    - more path cells stay inside the maze
    - and ideally the last path cell reaches the exit
    """
    if not path:
        return False

    top_left_cells = build_path_cells(start, path, False)
    bottom_left_cells = build_path_cells(start, path, True)

    top_left_score = count_cells_inside_maze(top_left_cells, width, height)
    bottom_left_score = count_cells_inside_maze(bottom_left_cells, width, height)

    # Big bonus if the path reaches the exit
    if top_left_cells[-1] == exit_position:
        top_left_score += 1000

    if bottom_left_cells[-1] == exit_position:
        bottom_left_score += 1000

    return bottom_left_score > top_left_score


def maze_coord_to_canvas_coord(
    x: int,
    y: int,
    height: int,
    use_bottom_left_system: bool
) -> tuple[int, int]:
    """
    Convert maze coordinates to canvas coordinates.

    Maze coordinate:
        one coordinate for each cell

    Canvas coordinate:
        bigger grid used for drawing walls and corridors

    Why multiply by 2?
        Because between two cells there is a wall position.
    """
    if use_bottom_left_system:
        row = height - 1 - y
    else:
        row = y

    canvas_row = row * 2 + 1
    canvas_col = x * 2 + 1

    return canvas_row, canvas_col


# ============================================================
# CANVAS BUILDING
# ============================================================
# The canvas is a bigger grid used only for drawing.
#
# Example:
# If maze is 5x5:
# Canvas is 11x11
#
# Maze cells are placed at:
#   row * 2 + 1
#   col * 2 + 1
#
# Walls are between cells.
# ============================================================

def build_empty_canvas(width: int, height: int) -> list[list[str]]:
    """
    Create a canvas full of walls.

    Later we open corridors inside this canvas.
    """
    canvas_height = height * 2 + 1
    canvas_width = width * 2 + 1

    canvas = []

    for _ in range(canvas_height):
        row = []

        for _ in range(canvas_width):
            row.append("wall")

        canvas.append(row)

    return canvas


def open_cell_and_passages(
    canvas: list[list[str]],
    cell: int,
    row: int,
    col: int
) -> None:
    """
    Open the current cell and its passages.

    If a wall does NOT exist, we open that direction.
    """
    canvas_row = row * 2 + 1
    canvas_col = col * 2 + 1

    # Open the center of the cell
    canvas[canvas_row][canvas_col] = "empty"

    # Open north passage
    if not has_wall(cell, NORTH):
        canvas[canvas_row - 1][canvas_col] = "empty"

    # Open south passage
    if not has_wall(cell, SOUTH):
        canvas[canvas_row + 1][canvas_col] = "empty"

    # Open west passage
    if not has_wall(cell, WEST):
        canvas[canvas_row][canvas_col - 1] = "empty"

    # Open east passage
    if not has_wall(cell, EAST):
        canvas[canvas_row][canvas_col + 1] = "empty"


def draw_solution_path(
    canvas: list[list[str]],
    start: tuple[int, int],
    path: str,
    width: int,
    height: int,
    use_bottom_left_system: bool
) -> None:
    """
    Draw the solution path on the canvas.

    We draw:
    - the cell itself
    - the small passage between two cells
    """
    path_cells = build_path_cells(start, path, use_bottom_left_system)

    for index, current_cell in enumerate(path_cells):
        x, y = current_cell

        if not (0 <= x < width and 0 <= y < height):
            continue

        current_row, current_col = maze_coord_to_canvas_coord(
            x,
            y,
            height,
            use_bottom_left_system
        )

        canvas[current_row][current_col] = "path"

        # Also fill the gap between previous cell and current cell
        if index > 0:
            previous_x, previous_y = path_cells[index - 1]

            if 0 <= previous_x < width and 0 <= previous_y < height:
                previous_row, previous_col = maze_coord_to_canvas_coord(
                    previous_x,
                    previous_y,
                    height,
                    use_bottom_left_system
                )

                middle_row = (current_row + previous_row) // 2
                middle_col = (current_col + previous_col) // 2

                canvas[middle_row][middle_col] = "path"


def open_maze_border(
    canvas: list[list[str]],
    x: int,
    y: int,
    width: int,
    height: int,
    use_bottom_left_system: bool
) -> None:
    """
    Open the border if start or exit is on the edge.

    This makes entry and exit visually connected to outside.
    """
    canvas_row, canvas_col = maze_coord_to_canvas_coord(
        x,
        y,
        height,
        use_bottom_left_system
    )

    # Left border
    if x == 0:
        canvas[canvas_row][0] = "empty"

    # Right border
    elif x == width - 1:
        canvas[canvas_row][len(canvas[0]) - 1] = "empty"

    # Bottom-left coordinate system
    if use_bottom_left_system:
        if y == 0:
            canvas[len(canvas) - 1][canvas_col] = "empty"
        elif y == height - 1:
            canvas[0][canvas_col] = "empty"

    # Top-left coordinate system
    else:
        if y == 0:
            canvas[0][canvas_col] = "empty"
        elif y == height - 1:
            canvas[len(canvas) - 1][canvas_col] = "empty"


def build_canvas(maze, show_path: bool) -> list[list[str]]:
    """
    Build the final drawable canvas.

    This function:
    1) Reads the maze grid
    2) Creates a wall-filled canvas
    3) Opens corridors
    4) Draws solution path if enabled
    5) Draws start and exit
    """
    grid = get_maze_grid(maze)

    height = len(grid)
    width = len(grid[0])

    start = get_start_position(maze)
    exit_position = get_exit_position(maze)
    path = get_solution_path(maze)

    use_bottom_left_system = should_use_bottom_left_system(
        start,
        exit_position,
        path,
        width,
        height
    )

    canvas = build_empty_canvas(width, height)

    # Open maze cells and passages
    for row in range(height):
        for col in range(width):
            cell = grid[row][col]
            open_cell_and_passages(canvas, cell, row, col)

    # Draw solution path only if show_path is True
    if show_path and path:
        draw_solution_path(
            canvas,
            start,
            path,
            width,
            height,
            use_bottom_left_system
        )

    # Draw start position
    start_x, start_y = start

    if 0 <= start_x < width and 0 <= start_y < height:
        start_row, start_col = maze_coord_to_canvas_coord(
            start_x,
            start_y,
            height,
            use_bottom_left_system
        )

        canvas[start_row][start_col] = "start"

        open_maze_border(
            canvas,
            start_x,
            start_y,
            width,
            height,
            use_bottom_left_system
        )

    # Draw exit position
    exit_x, exit_y = exit_position

    if 0 <= exit_x < width and 0 <= exit_y < height:
        exit_row, exit_col = maze_coord_to_canvas_coord(
            exit_x,
            exit_y,
            height,
            use_bottom_left_system
        )

        canvas[exit_row][exit_col] = "exit"

        open_maze_border(
            canvas,
            exit_x,
            exit_y,
            width,
            height,
            use_bottom_left_system
        )

    return canvas


# ============================================================
# PRINTING THE CANVAS
# ============================================================

def print_canvas(
    canvas: list[list[str]],
    wall_color: str
) -> None:
    """
    Print the canvas to the terminal using colored blocks.
    """
    for row in canvas:
        line = ""

        for item in row:
            if item == "wall":
                line += print_block(wall_color)

            elif item == "empty":
                line += print_block(BLACK_BG)

            elif item == "path":
                line += print_block(GRAY_BG)

            elif item == "start":
                line += print_block(MAGENTA_BG)

            elif item == "exit":
                line += print_block(RED_BG)

            else:
                line += print_block(BLACK_BG)

        print(line)


# ============================================================
# RE-GENERATE HELPERS
# ============================================================
# We do not want to edit maze.py.
#
# So, if maze.re_generate() is broken, this visualizer tries to
# reset common generator attributes and then calls maze.generate().
# ============================================================

def reset_maze_object(maze) -> None:
    """
    Reset common maze attributes before generating again.

    This is useful for MazeGenerator-style objects.
    """
    if not hasattr(maze, "width") or not hasattr(maze, "height"):
        return

    width = maze.width
    height = maze.height

    if hasattr(maze, "grid"):
        maze.grid = [[15] * width for _ in range(height)]

    if hasattr(maze, "visited"):
        maze.visited = [[False] * width for _ in range(height)]

    if hasattr(maze, "solution_path"):
        maze.solution_path = []

    if hasattr(maze, "mask"):
        maze.mask = set()

    if hasattr(maze, "pattern_grid"):
        maze.pattern_grid = []

    if hasattr(maze, "size_warning"):
        maze.size_warning = ""

    # Change seed so the new maze is different
    if hasattr(maze, "seed"):
        maze.seed = random.randint(1, 99999)


def regenerate_maze(maze) -> None:
    """
    Re-generate maze without editing maze.py.

    First we try:
        maze.re_generate()

    If it fails, we try:
        reset maze attributes
        maze.generate()
    """
    if hasattr(maze, "re_generate"):
        try:
            maze.re_generate()
            return
        except Exception:
            pass

    reset_maze_object(maze)

    if hasattr(maze, "generate"):
        maze.generate()
        return

    raise ValueError("Maze cannot be regenerated.")


# ============================================================
# MAIN VISUALIZER LOOP
# ============================================================

def visualize(maze: Maze) -> None:
    """
    Main visualization function.

    This function:
    - shows the maze
    - waits for user input
    - updates the screen
    """
    show_path = True
    color_index = 0

    while True:
        clear_screen()

        print("=== A-Maze-ing ===\n")

        try:
            canvas = build_canvas(maze, show_path)
            print_canvas(canvas, WALL_COLORS[color_index])
        except Exception as error:
            print(f"Visualize error: {error}")

        print("\nOptions:")
        print("1 - Re-generate maze")

        if show_path:
            print("2 - Hide path from entry to exit [ON]")
        else:
            print("2 - Show path from entry to exit [OFF]")

        print("3 - Rotate maze colors")
        print("4 - Quit")

        choice = input("\nChoice (1-4): ").strip()

        if choice == "1":
            try:
                regenerate_maze(maze)
            except Exception as error:
                input(f"\nRe-generate error: {error}\nPress Enter...")

        elif choice == "2":
            show_path = not show_path

        elif choice == "3":
            color_index += 1

            if color_index >= len(WALL_COLORS):
                color_index = 0

        elif choice == "4":
            break

        else:
            input("\nInvalid option. Press Enter...")