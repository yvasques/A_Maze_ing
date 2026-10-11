"""Module responsible for writing maze output files."""

from typing import List, Tuple


def write_maze_file(
    filepath: str,
    grid: List[List[int]],
    entry: Tuple[int, int],
    exit_coords: Tuple[int, int],
    shortest_path: str = "",
) -> None:
    """Save the generated maze and its metadata into a formatted
    output file.
    Args:
        filepath: Path to the output text file.
        grid: 2D matrix representing cell wall bitmasks (0-15).
        entry: Coordinates (x, y) of the maze entrance.
        exit_coords: Coordinates (x, y) of the maze exit.
        shortest_path: String of directions representing the solution path.
    """
    with open(filepath, "w", encoding="utf=8") as file:
        for row in grid:
            hex_row = ""
            for cell in row:
                hex_row += f"{cell:X}"
            file.write(f"{hex_row}\n")
        file.write("\n")

        file.write(f"{entry[0]}, {entry[1]} # entry (x,y)\n")
        file.write(f"{exit_coords[0]}, {exit_coords[1]} # exit (x,y)\n")
        file.write(f"{shortest_path}\n")
        file.write("user@42 ~/a_maze_ing$")
