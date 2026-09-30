from maze_generator import *

def display_asc_format() -> None:
        """Print the maze as ASCII art based on each cell's wall bitmask."""

        for y in range(generator.height):
            top: str = "+"
            middle: str = ""

            for x in range(generator.width):
                cell: int = generator.grid[y][x]

                top += ("---" if cell & NORTH else  "   ") + '+'
                middle += ("|" if cell & WEST else " ") + "   "

            last_cell: int = generator.grid[y][generator.width - 1]
            middle += "|" if last_cell & EAST else " "

            print(top)
            print(middle)

        bottom: str = "+"
        for x in range(generator.width):
            bottom_cell: int = generator.grid[generator.height - 1][x]
            bottom += ("---" if bottom_cell & SOUTH else "   ") + "+"
        print(bottom)


if __name__ == "__main__":
    generator = MazeGenerator(width=5, height=5)
    generator.generate()
    generator.display_grid_console()
    print()
    display_asc_format()
