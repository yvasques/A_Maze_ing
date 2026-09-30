import sys
from config_parser import parse_config
from maze_generator import MazeGenerator
from maze_solver import MazeSolver
from output import write_maze_file


def main() -> None:
    """Run the main maze generation flow"""
    if len(sys.argv) < 2:
        print("Usage: python3 a_maze_ing.py <config_file")
        sys.exit(1)

        config_path = sys.orig_argv[1]
        config = parse_config(config_path)

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
        print("Maze sucessfully generated and written to"
              f"{config.output_file}")


if __name__ == "__main__":
    main()
