import sys
from config_parser import parse_config, ConfigError
from maze_generator import MazeGenerator
from maze_solver import MazeSolver
from output import write_maze_file
from display import display_asc_format


def main() -> None:
    """Run the main maze generation flow"""
    config_path = next((
        arg for arg in sys.argv if arg.endswith(".txt")))
    if config_path is None:
        print("Usage: python3 a_maze_ing.py <config_file>")
        sys.exit(1)
    try:
        config = parse_config(config_path)
    except ConfigError as err:
        print(f"Error in configuration file: {err}")
        sys.exit(1)

    generator = MazeGenerator(
        width=config.width,
        height=config.height,
        entry=config.entry,
        exit_coords=config.exit,
        perfect=config.perfect,
        seed=config.seed,
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
    print("Maze sucessfully generated and written to "
          f"{config.output_file}")
    display_asc_format(generator)


if __name__ == "__main__":
    main()
