"""Module responsible for pathfinding and solving the maze."""

from collections import deque
from typing import List, Tuple, Dict

NORTH: int = 1
EAST: int = 2
SOUTH: int = 4
WEST: int = 8


class MazeSolver:
    """Solves a maze grid by finding the shortest path from entry
    to exit.
    """
    def __init__(
            self,
            grid: List[List[int]],
            width: int,
            height: int,
            entry: Tuple[int, int],
            exit_coords: Tuple[int, int],
    ) -> None:
        """Initialize the solver with the generaetd maze grid and
        targets.
        """
        self.grid: List[List[int]] = grid
        self.width: int = width
        self.height: int = height
        self.entry: Tuple[int, int] = entry
        self.exit_coords: Tuple[int, int] = exit_coords

    def solve(self) -> str:
        """Find the shortest path from entry to exit using BFS.
        Returns:
            A string representing direction steps (e.g ""NNESW)."""
        if self.entry == self.exit_coords:
            return ""

        queue: deque[Tuple[int, int]] = deque([self.entry])
        visited: set[Tuple[int, int]] = {self.entry}
        parent: Dict[Tuple[int, int], Tuple[Tuple[int, int], str]] = {}
        moves = [
            (0, -1, NORTH, "N"),
            (1, 0, EAST, "E"),
            (0, 1, SOUTH, "S"),
            (-1, 0, WEST, "W"),
        ]
        found = False

        while queue:
            curr_x, curr_y = queue.popleft()
            if (curr_x, curr_y) == self.exit_coords:
                found = True
                break
            cell_walls = self.grid[curr_y][curr_x]
            for dx, dy, wall_mask, step_char in moves:
                if (cell_walls & wall_mask) == 0:
                    nx, ny = curr_x + dx, curr_y + dy
                    if 0 <= nx < self.width and 0 <= ny < self.height:
                        if (nx, ny) not in visited:
                            visited.add((nx, ny))
                            parent[(nx, ny)] = ((curr_x, curr_y), step_char)
                            queue.append((nx, ny))
        if not found:
            return ""

        path_chars: List[str] = []
        curr = self.exit_coords

        while curr != self.entry:
            prev_cell, direction_char = parent[curr]
            path_chars.append(direction_char)
            curr = prev_cell

        path_chars.reverse()
        return "".join(path_chars)
