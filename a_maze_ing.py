import sys
from typing import Optional, Tuple
from config_parser import parse_config, ConfigError, MazeConfig
from maze_generator import MazeGenerator
from maze_solver import MazeSolver
from output import write_maze_file


def build_maze(config: MazeConfig,
               seed: Optional[int]) -> Tuple[MazeGenerator, str]:
    """Generate a maze, solve it and write it to the output file.
    Args:
        config: The validated configuration.
        seed: Seed for the generation, or None for a random maze.
    Returns:
        The generator (with the grid) and the shortest path string.
    """

    generator = MazeGenerator(
        width=config.width,
        height=config.height,
        entry=config.entry,
        exit_coords=config.exit,
        perfect=config.perfect,
        seed=seed,
    )
    generator.generate()

    solver = MazeSolver(
        grid=generator.grid,
        width=config.width,
        height=config.height,
        entry=config.entry,
        exit_coords=config.exit,
    )
    shortest_path = solver.solve()

    write_maze_file(
        filepath=config.output_file,
        grid=generator.grid,
        entry=config.entry,
        exit_coords=config.exit,
        shortest_path=shortest_path,
    )

    return generator, shortest_path


def main() -> None:
    """Run the main maze generation flow."""
    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py <config_file>",
              file=sys.stderr)
        sys.exit(1)

    try:
        from display import MazeWindow
    except ImportError as err:
        print(f"Error: MLX is not available ({err}). "
              f"Run 'make install' and use 'make run'.",
              file=sys.stderr)
        sys.exit(1)

    try:
        config = parse_config(sys.argv[1])
        generator, path = build_maze(config, config.seed)
        print("Maze successfully generated and written to "
              f"{config.output_file}")
        window = MazeWindow(generator, path,
                            lambda: build_maze(config, None))
        window.run()
    except (ConfigError, ValueError, OSError) as err:
        print(f"Error: {err}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
