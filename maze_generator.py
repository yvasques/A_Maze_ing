"""Module responsible for maze generation and manipulation."""
from typing import List, Tuple, Optional

NORTH: int = 1
EAST: int = 2
SOUTH: int = 4
WEST: int = 8


class MazeGenerator:
    def __init__(
            self,
            width: int,
            height: int,
            entry: Tuple[int, int] = (0, 0),
            exit_coords: Tuple[int, int] = (0, 0),
            perfect: bool = False,
            seed: Optional[int] = None,
            ) -> None:
        """Initialize de maze configuration parameters.
        Args:
            width: Maze width in number of cells.
            height: Maze height in number of cells.
            entry: Entry coordinates as (x, y).
            exit_coords: Exit coordinates as (x, y).
            perfect: If true, generates a single unique path. Defauts to False.
            seed: Optional random seed for reproducibilty.
        """
        self.width: int = width
        self.height: int = height
        self.entry: Tuple[int, int] = entry
        self.exit_coords: Tuple[int, int] = exit_coords
        self.perfect: bool = perfect
        self.seed: Optional[int] = seed

        # Create a grid[y][x] initialized with 15 (all walls closed)
        self.grid: List[List[int]] = []
        for y in range(self.height):
            row: List[int] = []
            for x in range(self.width):
                row.append(15)
            self.grid.append(row)    

    def get_cell(self, x: int, y: int) -> int:
        """Get the wall bitmask value of a specific cell at (x, y)
        Args:
        x: Column index.
        y: Row index.

        Returns:
        An integer representing closed walls (0-15).
            """
        return self.grid[y][x]

    def display_grid_console(self) -> None:
        """Printando a matriz para teste"""
        for row in self.grid:
            print(row)

    def generate(self) -> None:
        """Generate de maze cells and wall structures"""
        # TODO Implementar algoritimo de gerar o labirinto
        pass

    def get_shortest_path(self) -> str:
        """Find and return the shortest path between entry and exit
        Returns a string representing the directions steps (Example:"NSEW")
        """
        # TODO Implementar algoritmo de achar o menor caminho
        return ""


if __name__ == "__main__":
    generator = MazeGenerator(width=5, height=5)
    generator.display_grid_console()
