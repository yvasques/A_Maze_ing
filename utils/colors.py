from random import choice

# Format 0xAARRGGBB (alpha FF = opaque)
WHITE: int = 0xFFFFFFFF
RED:   int = 0xFFFF0000
GREEN: int = 0xFF00FF00
BLUE:  int = 0xFF0000FF

WALL_COLORS: list[int] = [WHITE, RED, GREEN, BLUE]
