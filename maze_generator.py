"""Module responsible for maze generation and manipulation."""

from typing import List, Tuple, Optional
import random

NORTH: int = 1
EAST: int = 2
SOUTH: int = 4
WEST: int = 8

PATTERN_42 = [
    [1, 0, 0,  0,  1, 1, 1],
    [1, 0, 0,  0,  0, 0, 1],
    [1, 1, 1,  0,  1, 1, 1],
    [0, 0, 1,  0,  1, 0, 0],
    [0, 0, 1,  0,  1, 1, 1],
]


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
        self.grid: List[List[int]] = []
        self._reset_grid()
        self._rng = random.Random(seed)

        if width < 1 or height < 1:
            raise ValueError("width and height must be at least 1")
        for name, (x, y) in (("entry", entry), ("exit", exit_coords)):
            if not (0 <= x < width and 0 <= y < height):
                raise ValueError(f"{name} {(x, y)} is out of bounds")
        if entry == exit_coords:
            raise ValueError("entry and exit must be different")

    def _reset_grid(self) -> None:
        """Reset de maze grid with all the walls closed"""
        self.grid = [[15] * self.width for _ in range(self.height)]

    def get_cell(self, x: int, y: int) -> int:
        """Get the wall bitmask value of a specific cell at (x, y)
        Args:
            x: Column index.
            y: Row index.
        Returns:
            An integer representing closed walls (0-15).
        """
        return self.grid[y][x]

    def remove_wall(self, x: int, y: int, direction: int) -> None:
        """
        Remove a specific wall from a cell at (x, y) using bitwise operations.
            Args:
                x: Column index.
                y: Row index.
                direction: Wall constant (NORTH, EAST, SOUTH, WEST).
        """
        self.grid[y][x] = self.grid[y][x] & (~direction)

    def remove_wall_between(self, x1: int, y1: int, x2: int, y2: int) -> None:
        """
        Remove shared walls between two adjacent cells (x1, y1) and (x2, y2).
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

    def _get_42_cells(self) -> List[Tuple[int, int]]:
        """Calculate real coordinates (x,y) on the grid corresponding to
        the 42 pattern"""
        pattern_h = len(PATTERN_42)
        pattern_w = len(PATTERN_42[0])

        if self.width < pattern_w + 2 or self.height < pattern_h + 2:
            return []

        start_x = (self.width - pattern_w) // 2
        start_y = (self.height - pattern_h) // 2
        cells_42 = []
        for py in range(pattern_h):
            for px in range(pattern_w):
                if PATTERN_42[py][px] == 1:
                    cells_42.append((start_x + px, start_y + py))
        return cells_42

    def _is_dead_end(self, x: int, y: int) -> bool:
        """Check if a cell is a dead-end (has 3 closed walls).
        (Ignores the dead ends in the 42 pattern)"""
        if (x, y) in set(self._get_42_cells()):
            return False
        return bin(self.grid[y][x]).count("1") == 3

    def _is_wall_between_closed(self, x1: int, y1: int,
                                x2: int, y2: int) -> bool:
        """Check if the wall between two adjacent cells is closed."""
        dx, dy = x2 - x1, y2 - y1
        if dx == 1:
            return bool(self.grid[y1][x1] & EAST)
        if dx == -1:
            return bool(self.grid[y1][x1] & WEST)
        if dy == 1:
            return bool(self.grid[y1][x1] & SOUTH)
        if dy == -1:
            return bool(self.grid[y1][x1] & NORTH)
        return False

    def _ensure_open_cell(self, x: int, y: int) -> None:
        """Ensure a cell has at least two open passageways"""
        neighbors = self.get_neighbors(x, y)
        open_passages = 4 - bin(self.grid[y][x]).count("1")
        for nx, ny in neighbors:
            if open_passages >= 2:
                break
            if self._is_wall_between_closed(x, y, nx, ny):
                self.remove_wall_between(x, y, nx, ny)
                open_passages += 1

    def _open_corners_and_center(self) -> None:
        """Open corridors at the four corners and center for Pac-Man mode."""
        cells_42 = set(self._get_42_cells())
        targets = [
            (0, 0),
            (self.width - 1, 0),
            (0, self.height - 1),
            (self.width - 1, self.height - 1),
        ]
        center = (self.width // 2, self.height // 2)

        if center not in cells_42:
            targets.append(center)

        for cx, cy in targets:
            self._ensure_open_cell(cx, cy)

    def _eliminate_dead_ends(self) -> None:
        """Eliminate dead-ends across the grid without breaking
       the 42 pattern."""
        cells_42 = set(self._get_42_cells())
        while True:
            removed_any = False
            for y in range(self.height):
                for x in range(self.width):
                    if (x, y) in cells_42:
                        continue
                    if self._is_dead_end(x, y):
                        valid_neighbors = [
                            (nx, ny)
                            for nx, ny in self.get_neighbors(x, y)
                            if (nx, ny) not in cells_42
                        ]
                        self._rng.shuffle(valid_neighbors)

                        for nx, ny in valid_neighbors:
                            if self._is_wall_between_closed(x, y, nx, ny):
                                self.remove_wall_between(x, y, nx, ny)
                                removed_any = True
                                break
            if not removed_any:
                break

    def generate(self) -> None:
        """Generate the maze cells and wall structures using DFS"""
        self._reset_grid()

        visited = [[False] * self.width for _ in range(self.height)]

        cells_42 = set(self._get_42_cells())
        for (cx, cy) in cells_42:
            visited[cy][cx] = True
            self.grid[cy][cx] = 15

        start_x, start_y = self.entry
        visited[start_y][start_x] = True
        stack = [(start_x, start_y)]

        while stack:
            x, y = stack[-1]
            unvisited = [(un_x, un_y) for un_x, un_y
                         in self.get_neighbors(x, y)
                         if not visited[un_y][un_x]]

            if unvisited:
                un_x, un_y = self._rng.choice(unvisited)
                self.remove_wall_between(x, y, un_x, un_y)
                visited[un_y][un_x] = True
                stack.append((un_x, un_y))
            else:
                stack.pop()

        if not self.perfect:
            self._open_corners_and_center()
            self._eliminate_dead_ends()
