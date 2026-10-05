from maze_generator import (MazeGenerator,
                            NORTH, WEST, EAST, SOUTH)
from mlx import Mlx
from typing import Any, Tuple

from utils.colors import RED, WHITE, GREEN, BLUE


CELL_SIZE: int = 32
WALL_SIZE: int = 3
MARGIN: int = 20

KEY_4: int = 52

MENU_TEXT: str = "1: regen   2: path   3: color   4: quit"


class MazeWindow:
    """Window that draws a maze using the MiniLibX library."""

    def __init__(self, maze: MazeGenerator) -> None:
        """Create the MLX window sized to fit the maze.
        Args:
            maze: The generated maze to display.
        """

        self.maze: MazeGenerator = maze
        self.mlx: Any = Mlx()
        self.mlx_ptr: Any = self.mlx.mlx_init() #begin mlx
        self.win_ptr: Any = self.mlx.mlx_new_window(
            self.mlx_ptr,
            maze.width * CELL_SIZE + 2 * MARGIN,
            maze.height * CELL_SIZE + 2 * MARGIN + 30,
            "A_Maze_ing"
        ) #open window


    def _origin(self, x: int, y: int) -> Tuple[int, int]:
        """Return the pixel position of the top-left corner of a cell."""
        return MARGIN + x * CELL_SIZE, MARGIN + y * CELL_SIZE

    def _draw_rect(self, x: int, y: int, w: int, h: int) -> None:
        """Fill a rectangle of pixels with the wall color."""
        for py in range(y, y + h):
            for px in range(x, x + w):
                self.mlx.mlx_pixel_put(self.mlx_ptr, self.win_ptr,
                                       px, py, BLUE)

    def _cell_label(self, x: int, y: int) -> str:
        """Return the letter of a cell (entry, exit or empty)."""
        if (x, y) == self.maze.entry:
            return "E"
        if (x, y) == self.maze.exit_coords:
            return "S"
        return ""

    def _horizontal_walls(self, y: int, wall: int) -> None:
        """Draw the horizontal walls (NORTH or SOUTH) of row y."""
        offset: int = CELL_SIZE if wall == SOUTH else 0
        for x in range(self.maze.width):
            if self.maze.get_cell(x, y) & wall:
                px, py = self._origin(x, y)
                self._draw_rect(px, py + offset,
                                CELL_SIZE + WALL_SIZE, WALL_SIZE)

    def _middle_line(self, y: int) -> None:
        """Build the line containing cell labels and vertical walls."""
        for x in range(self.maze.width):
            if self.maze.get_cell(x, y) & WEST:
                px, py = self._origin(x, y)
                self._draw_rect(px, py, WALL_SIZE, CELL_SIZE + WALL_SIZE)

            label: str = self._cell_label(x, y)
            if label:
                self.mlx.mlx_string_put(self.mlx_ptr,
                                        self.win_ptr, px, py, WHITE, label)

        east_x:int  = self.maze.width - 1
        if self.maze.get_cell(east_x, y) & EAST:
            px, py = self._origin(east_x, y)
            self._draw_rect(px + CELL_SIZE, py, WALL_SIZE, CELL_SIZE + WALL_SIZE)


    def _draw_menu(self):
        """Write the menu text below the maze."""
        menu_y: int = self.maze.height * CELL_SIZE + 2 * MARGIN

        self.mlx.mlx_string_put(self.mlx_ptr, self.win_ptr, MARGIN,
                                menu_y, GREEN, MENU_TEXT)


    def _on_key(self, keycode: int, param: Any) -> None:
        if keycode == KEY_4:
            self._close_window(Any)
            return
        self.draw()


    def _close_window(self,param: Any):
        """Stop the event loop when the window is closed."""
        self.mlx.mlx_loop_exit(self.mlx_ptr)


    def draw(self) -> None:
            """Draw the whole maze based on each cell's wall bitmask."""
            for y in range(self.maze.height):
                self._horizontal_walls(y, NORTH)
                self._middle_line(y)
            self._horizontal_walls(self.maze.height -1, SOUTH)
            self._draw_menu()

    def run(self) -> None:
        self.draw()
        self.mlx.mlx_key_hook(self.win_ptr, self._on_key, None)
        self.mlx.mlx_loop(self.mlx_ptr)
