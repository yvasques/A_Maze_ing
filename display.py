from maze_generator import (MazeGenerator,
                            NORTH, WEST, EAST, SOUTH)
import utils.colors as colors
import utils.keys_menu as keys
from mlx import Mlx  # type: ignore
from typing import Any, Tuple, Set, Dict
from config_parser import MazeConfig

CELL_SIZE: int = 32
WALL_SIZE: int = 3
MARGIN: int = 20
MIN_WIN_WIDTH: int = 700
MIN_WIN_HEIGHT: int = 700
MENU_HEIGHT: int = 40

MOVES: Dict[str, Tuple[int, int]] = {"N": (0, -1),
                                     "E": (1, 0),
                                     "S": (0, 1),
                                     "W": (-1, 0)}


class MazeWindow:
    """Window that draws a maze using the MiniLibX library."""

    def __init__(self, maze: MazeGenerator, path: str,
                 config: MazeConfig) -> None:
        """Create the MLX window sized to fit the maze.
        Args:
            maze: The generated maze to display.
        """

        self.maze: MazeGenerator = maze
        self.color_index: int = 2
        self.color_42_index: int = 6
        self.path: str = path
        self.config: MazeConfig = config
        self.show_path: bool = False

        calc_width: int = maze.width * CELL_SIZE + 2 * MARGIN
        calc_height: int = maze.height * CELL_SIZE + 2 * MARGIN

        self.win_width: int = max(calc_width, MIN_WIN_WIDTH)
        self.win_height: int = max(calc_height, MIN_WIN_HEIGHT)

        maze_pixel_w: int = maze.width * CELL_SIZE
        maze_pixel_h: int = maze.height * CELL_SIZE

        self.offset_x: int = (self.win_width - maze_pixel_w) // 2
        self.offset_y: int = ((self.win_height - MENU_HEIGHT) - maze_pixel_h) // 2

        self.mlx: Any = Mlx()
        self.mlx_ptr: Any = self.mlx.mlx_init()
        self.win_ptr: Any = self.mlx.mlx_new_window(
            self.mlx_ptr,
            self.win_width,
            self.win_height,
            "A_Maze_ing"
        )

    def _origin(self, x: int, y: int) -> Tuple[int, int]:
        """Return the pixel position of the top-left corner of a cell."""
        return self.offset_x + x * CELL_SIZE, self.offset_y + y * CELL_SIZE

    def _draw_rect(self, x: int, y: int, w: int, h: int, color: int) -> None:
        """Fill a rectangle of pixels with the wall color."""
        for py in range(y, y + h):
            for px in range(x, x + w):
                self.mlx.mlx_pixel_put(self.mlx_ptr, self.win_ptr,
                                       px, py, color)

    def _draw_endpoints(self) -> None:
        """Draw colored tiles for entry and exit points."""
        padding: int = 4
        size: int = CELL_SIZE - (2 * padding)

        ex, ey = self.maze.entry
        px, py = self._origin(ex, ey)
        self._draw_rect(px + padding, py + padding, size, size, colors.GREEN)

        sx, sy = self.maze.exit_coords
        px, py = self._origin(sx, sy)
        self._draw_rect(px + padding, py + padding, size, size, colors.RED)

    def _horizontal_walls(self, y: int, wall: int) -> None:
        """Draw the horizontal walls (NORTH or SOUTH) of row y."""
        color: int = colors.WALL_COLORS[self.color_index]
        offset: int = CELL_SIZE if wall == SOUTH else 0
        for x in range(self.maze.width):
            if self.maze.get_cell(x, y) & wall:
                px, py = self._origin(x, y)
                self._draw_rect(px, py + offset,
                                CELL_SIZE + WALL_SIZE, WALL_SIZE, color)

    def _middle_line(self, y: int) -> None:
        """Build the line containing cell labels and vertical walls."""
        color: int = colors.WALL_COLORS[self.color_index]
        for x in range(self.maze.width):
            if self.maze.get_cell(x, y) & WEST:
                px, py = self._origin(x, y)
                self._draw_rect(px, py, WALL_SIZE,
                                CELL_SIZE + WALL_SIZE, color)

        east_x: int = self.maze.width - 1
        if self.maze.get_cell(east_x, y) & EAST:
            px, py = self._origin(east_x, y)
            self._draw_rect(px + CELL_SIZE, py, WALL_SIZE,
                            CELL_SIZE + WALL_SIZE, color)

    def _draw_path_cells(self) -> Set[Tuple[int, int]]:
        """Convert the path string into the set of cells it crosses."""
        (x, y) = self.maze.entry
        cells: Set[Tuple[int, int]] = {(x, y)}
        for step in self.path:
            px, py = MOVES[step]
            x, y = px + x, py + y
            cells.add((x, y))
        return cells

    def _draw_path(self) -> None:
        """Draw a small square in the center of each cell of the path."""
        size: int = CELL_SIZE // 3
        offset: int = (CELL_SIZE - size) // 2
        for (x, y) in self._draw_path_cells():
            if (x, y) == self.maze.entry or (x, y) == self.maze.exit_coords:
                continue
            px, py = self._origin(x, y)
            self._draw_rect(px + offset, py + offset, size, size, 0xFFFFD700)

    def _draw_menu(self) -> None:
        """Write the menu text below the maze."""
        menu_y: int = self.win_height - 25
        menu_x: int = MARGIN

        self.mlx.mlx_string_put(self.mlx_ptr, self.win_ptr, menu_x,
                                menu_y, colors.GREEN, keys.MENU_TEXT)

    def _on_key(self, keycode: int, param: Any) -> None:
        if keycode == keys.KEY_1:
            import random
            from a_maze_ing import build_maze
            random.seed()
            self.maze, self.path = build_maze(self.config, seed=None)
            self.draw()
            return

        if keycode == keys.KEY_2:
            self.show_path = not self.show_path
            self.draw()
            return

        if keycode == keys.KEY_3:
            self.color_index = (self.color_index + 1) % len(colors.WALL_COLORS)

        if keycode == keys.KEY_4:
            self.color_42_index = (
                (self.color_42_index + 1) % len(colors.WALL_COLORS)
            )
        if keycode in (keys.KEY_ESC_MAC, keys.KEY_ESC_LINUX, keys.KEY_5):
            self._close_window(Any)
            return
        self.draw()

    def _close_window(self, param: Any):
        """Stop the event loop when the window is closed."""
        self.mlx.mlx_loop_exit(self.mlx_ptr)

    def _draw_42_pattern(self) -> None:
        """Print 42 patterns cells on a stand-out colour"""
        cells_42 = self.maze._get_42_cells()
        color_42 = colors.WALL_COLORS[self.color_42_index]
        for (x, y) in cells_42:
            px, py = self._origin(x, y)
            self._draw_rect(px, py, CELL_SIZE, CELL_SIZE, color_42)

    def draw(self) -> None:
        """Draw the whole maze based on each cell's wall bitmask."""
        self.mlx.mlx_clear_window(self.mlx_ptr, self.win_ptr)
        self._draw_endpoints()

        if self.show_path:
            self._draw_path()

        self._draw_42_pattern()
        for y in range(self.maze.height):
            self._horizontal_walls(y, NORTH)
            self._middle_line(y)
        self._horizontal_walls(self.maze.height - 1, SOUTH)
        self._draw_menu()

    def run(self) -> None:
        self.draw()
        self.mlx.mlx_key_hook(self.win_ptr, self._on_key, None)
        self.mlx.mlx_loop(self.mlx_ptr)
