from maze_generator import (MazeGenerator,
                            NORTH, WEST, EAST, SOUTH)


def _cell_label(maze: MazeGenerator, x: int, y: int) -> str:
    """Return the 3-char label of a cell (entry, exit or empty)."""
    if (x, y) == maze.entry:
        return " E "
    if (x, y) == maze.exit_coords:
        return " S "
    return "   "


def _horizontal_line(maze: MazeGenerator, y: int, wall: int) -> str:
    """Build a horizontal border line using the given wall flag."""
    line: str = "+"
    for x in range(maze.width):
        has_wall: bool = bool(maze.get_cell(x, y) & wall)
        line += ("---" if has_wall else "   ") + "+"
    return line


def _middle_line(maze: MazeGenerator, y: int) -> str:
    """Build the line containing cell labels and vertical walls."""
    line: str = ""
    for x in range(maze.width):
        has_west: bool = bool(maze.get_cell(x, y) & WEST)
        line += ("|" if has_west else " ") + _cell_label(maze, x, y)

    has_east: bool = bool(maze.get_cell(maze.width - 1, y) & EAST)
    line += "|" if has_east else " "
    return line


def display_asc_format(maze: MazeGenerator) -> None:
    """Print the maze in ASCII format."""
    for y in range(maze.height):
        print(_horizontal_line(maze, y, NORTH))
        print(_middle_line(maze, y))
    print(_horizontal_line(maze, maze.height - 1, SOUTH))
