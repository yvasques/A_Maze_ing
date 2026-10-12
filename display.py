from maze_generator import (MazeGenerator,
                            NORTH, WEST, EAST, SOUTH)
from utils.colors import WALL_COLORS, GREEN, RED
from utils.keys_menu import (KEY_1, KEY_2, KEY_3, KEY_4,
                             KEY_5, KEY_ESC_LINUX,
                             KEY_ESC_MAC, MENU_TEXT)
from mlx import Mlx
from typing import Any, Tuple, Dict, Callable
import time


CELL_SIZE: int = 32
WALL_SIZE: int = 3
MARGIN: int = 20
MIN_WIN_WIDTH: int = 700
MIN_WIN_HEIGHT: int = 700
MENU_HEIGHT: int = 40
PATH_ANIMATION_INTERVAL: float = 0.08

MOVES: Dict[str, Tuple[int, int]] = {"N": (0, -1),
                                     "E": (1, 0),
                                     "S": (0, 1),
                                     "W": (-1, 0)}


class MazeWindow:
    """Window that draws a maze using the MiniLibX library."""

    def __init__(self, maze: MazeGenerator, path: str,
                 regenerate: Callable[[], Tuple[MazeGenerator, str]]) -> None:
        """Create the MLX window sized to fit the maze.
        Args:
            maze: The generated maze to display.
        """

        self.maze: MazeGenerator = maze
        self.color_index: int = 2
        self.color_42_index: int = 6
        self.path: str = path
        self.show_path: bool = False
        self.path_cells: list[Tuple[int, int]] = []
        self.path_progress:int = 0
        self.last_path_animation_time: float = 0.0
        self.regenerate: Callable[[], Tuple[MazeGenerator, str]] = regenerate

        calc_width: int = maze.width * CELL_SIZE + 2 * MARGIN
        calc_height: int = maze.height * CELL_SIZE + 2 * MARGIN

        self.win_width: int = max(calc_width, MIN_WIN_WIDTH)
        self.win_height: int = max(calc_height, MIN_WIN_HEIGHT)

        maze_pixel_w: int = maze.width * CELL_SIZE
        maze_pixel_h: int = maze.height * CELL_SIZE

        self.offset_x: int = (self.win_width - maze_pixel_w) // 2
        self.offset_y: int = (
            (self.win_height - MENU_HEIGHT) - maze_pixel_h) // 2

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
        self._draw_rect(px + padding, py + padding, size, size, GREEN)

        sx, sy = self.maze.exit_coords
        px, py = self._origin(sx, sy)
        self._draw_rect(px + padding, py + padding, size, size, RED)

    def _horizontal_walls(self, y: int, wall: int) -> None:
        """Draw the horizontal walls (NORTH or SOUTH) of row y."""
        color: int = WALL_COLORS[self.color_index]
        offset: int = CELL_SIZE if wall == SOUTH else 0
        for x in range(self.maze.width):
            if self.maze.get_cell(x, y) & wall:
                px, py = self._origin(x, y)
                self._draw_rect(px, py + offset,
                                CELL_SIZE + WALL_SIZE, WALL_SIZE, color)

    def _middle_line(self, y: int) -> None:
        """Build the line containing cell labels and vertical walls."""
        color: int = WALL_COLORS[self.color_index]
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

    def _get_path_cells(self) -> list[Tuple[int, int]]:
            """Return the path cells in the order they are visited for animation."""
            x,y = self.maze.entry
            cells:list[Tuple[int, int]] = [(x,y)]

            for step in self.path:
                dx, dy = MOVES[step]
                x += dx
                y += dy
                cells.append((x,y))
            return cells

    def _draw_path(self) -> None:
        """Draw a small square in the center of each cell of the path."""
        size: int = CELL_SIZE // 3
        offset: int = (CELL_SIZE - size) // 2

        for (x, y) in self.path_cells[:self.path_progress]:
            if (x, y) == self.maze.entry or (x, y) == self.maze.exit_coords:
                continue

            px, py = self._origin(x, y)
            self._draw_rect(px + offset, py + offset, size, size, 0xFFFFD700)

    def _animate_path(self, param: Any) -> None:
        """Reveal one more path cell at a fixed time interval."""
        if not self.show_path:
            return

        now: float = time.monotonic()
        if now - self.last_path_animation_time < PATH_ANIMATION_INTERVAL:
            return

        self.last_path_animation_time = now

        if self.path_progress < len(self.path_cells):
            self.path_progress += 1
            self.draw()

    def _restart_animation_path(self) -> None:
        self.path_cells = self._get_path_cells()
        self.path_progress = 0
        self.last_path_animation_time = time.monotonic()

    def _draw_menu(self) -> None:
        """Write the menu text below the maze."""
        menu_y: int = self.win_height - 25
        menu_x: int = MARGIN

        self.mlx.mlx_string_put(self.mlx_ptr, self.win_ptr, menu_x,
                                menu_y, GREEN, MENU_TEXT)

    def _on_key(self, keycode: int, param: Any) -> None:
        if keycode == KEY_1:
            try:
                self.maze, self.path = self.regenerate()
                self._restart_animation_path()
            except (ValueError, OSError) as err:
                print(f"Error: {err}")

        elif keycode == KEY_2:
            self.show_path = not self.show_path
            if self.show_path:
                self._restart_animation_path()
            else:
                self.path_progress = 0
            self.draw()
            return

        elif keycode == KEY_3:
            self.color_index = (self.color_index + 1) % len(WALL_COLORS)

        elif keycode == KEY_4:
            self.color_42_index = (self.color_42_index + 1) % len(
                WALL_COLORS)
        elif keycode in (KEY_ESC_MAC, KEY_ESC_LINUX, KEY_5):
            self._close_window(Any)
            return
        self.draw()

    def _close_window(self, param: Any) -> None:
        """Stop the event loop when the window is closed."""
        self.mlx.mlx_loop_exit(self.mlx_ptr)

    def _draw_42_pattern(self) -> None:
        """Print 42 patterns cells on a stand-out colour"""
        cells_42 = self.maze._get_42_cells()
        color_42 = WALL_COLORS[self.color_42_index]
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
        """Run the maze"""
        self.draw()
        self.mlx.mlx_expose_hook(self.win_ptr, lambda p: self.draw(), None)
        self.mlx.mlx_key_hook(self.win_ptr, self._on_key, None)
        self.mlx.mlx_hook(self.win_ptr, 33, 0, self._close_window, None)
        self.mlx.mlx_loop_hook(self.mlx_ptr, self._animate_path, None)
        self.mlx.mlx_loop(self.mlx_ptr)
