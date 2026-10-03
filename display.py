from maze_generator import (MazeGenerator,
                            NORTH, WEST, EAST, SOUTH)


def _cell_label(maze: MazeGenerator, x: int, y: int) -> str:
        if (x, y) == maze.entry:
            return " E "
        elif (x, y) == maze.exit_coords:
            return " S "
        return "   "


def _horizontal_line(maze: MazeGenerator, y:int, wall: int) -> str:
    line: str = "+"
    for x in range(maze.width):
        has_wall: bool = bool(maze.get_cell(x, y) & wall)
        line += ("---" if has_wall else "   ") + "+"
    return line

def _middle_line(maze: MazeGenerator, y: int):
    line: str = ""
    for x in range(maze.width):
        has_west: bool = bool(maze.get_cell(x, y) & WEST)
        line += ("|" if has_west else " ") + _cell_label(maze, x, y)

    has_east: bool = bool(maze.get_cell(maze.width-1, y) & EAST)
    line += ("|" if has_east else " ")

    return line

def display_asc_format(maze: MazeGenerator) -> None:
    for y in range(maze.height):
        print(_horizontal_line(maze, y, NORTH))
        print(_middle_line(maze, y))
    print(_horizontal_line(maze, maze.height-1, SOUTH))



if __name__ == "__main__":
    generator = MazeGenerator(width=5, height=5,
                              entry=(0,0), exit_coords=(4,4))

    generator.generate()
