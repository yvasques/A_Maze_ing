from maze_generator import *


def display_asc_format(maze: MazeGenerator) -> None:
        """Print the maze as ASCII art based on each cell's wall bitmask."""

        for y in range(maze.height):
            top: str = "+"
            middle: str = ""

            for x in range(maze.width):
                cell: int = maze.grid[y][x]

                top += ("---" if cell & NORTH else  "   ") + '+'
                middle += ("|" if cell & WEST else " ") + maze.entry_exit(x, y)

            last_cell: int = maze.grid[y][maze.width - 1]
            middle += "|" if last_cell & EAST else " "

            print(top)
            print(middle)

        bottom: str = "+"
        for x in range(maze.width):
            bottom_cell: int = maze.grid[maze.height - 1][x]
            bottom += ("---" if bottom_cell & SOUTH else "   ") + "+"
        print(bottom)


if __name__ == "__main__":
    generator = MazeGenerator(width=8, height=5, entry=(0,0), exit_coords=(4,4))
    generator.generate()
    display_asc_format(generator)
