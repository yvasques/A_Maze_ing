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
        """Initialize the maze configuration parameters.
        Args:
            width: Maze width in number of cells.
            height: Maze height in number of cells.
            entry: Entry coordinates as (x, y).
            exit_coords: Exit coordinates as (x, y).
            perfect: If true, generates an unique path. Defaults to False.
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

    def remove_wall(self, x: int, y: int, direction: int) -> None:
        """Remove a specific wall from a cell at (x, y) using bitwise operations.
            Args:
                x: Column index.
                y: Row index.
                direction: Wall constant (NORTH, EAST, SOUTH, WEST).
        """
        self.grid[x][y] = self.grid[y][x] & (~direction)

    def remove_wall_between(self, x1: int, y1: int, x2: int, y2: int) -> None:
        """Remove shared walls between two adjacent cells (x1, y1) and (x2, y2).
            Args:
                x1: Column of first cell.
                y1: Row of first cell.
                x2: Column of second cell.
                y2: Row of second cell.
                """
        dx = x2 - x1
        dy = y2 - y1

        if dx == 1:
            self.remove_wall(x1, y1, EAST)
            self.remove_wall(x2, y2, WEST)
        elif dx == -1:
            self.remove_wall(x1, y1, WEST)
            self.remove_wall(x2, y2, EAST)
        elif dy == 1:
            self.remove_wall(x1, y1, SOUTH)
            self.remove_wall(x2, y2, NORTH)
        elif dy == -1:
            self.remove_wall(x1, y1, NORTH)
            self.remove_wall(x2, y2, SOUTH)

    def get_neighbors(self, x: int, y: int) -> List[Tuple[int, int]]:
        """Get coordinates of valid adjacent cells within maze boundaries.
            Args:
                x: Column index.
                y: Row index.
            Returns:
                List of (x, y) tuples for all valid adjacent neighbors.
        """
        neighbors: List[Tuple[int, int]] = []
        directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]

        for dx, dy in directions:
            new_x = x + dx
            new_y = y + dy
            if 0 <= new_x < self.width and 0 <= new_y < self.height:
                neighbors.append((new_x, new_y))
        return neighbors

    def generate(self) -> None:
        """Generate the maze cells and wall structures"""
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
    print("Grid inicial (tudo fechado = 15):")
    generator.display_grid_console()
    generator.remove_wall_between(0, 0, 1, 0)
    print("\nGrid após abrir parede entre (0,0) e (1,0):")
    generator.display_grid_console()
