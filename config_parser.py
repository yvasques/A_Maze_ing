from typing import Tuple, Dict
from dataclasses import dataclass
from pathlib import Path


class ConfigError(Exception):
    """Raised when the configuration file is invalid."""


@dataclass
class MazeConfig:
    width: int
    height: int
    entry: Tuple[int, int]
    exit: Tuple[int, int]
    output_file: str
    perfect: bool
    seed: int | None = None


REQUIRED_KEYS = {"WIDTH", "HEIGHT", "ENTRY", "EXIT", "PERFECT", "OUTPUT_FILE"}


def _read_raw_lines(path: Path) -> Dict[str, str]:
    """Read the config file and return raw key/value pairs as strings."""

    raw_dict: Dict[str, str] = {}
    try:
        with path.open('r', encoding='utf-8') as file:
            for line_number, line in enumerate(file, start=1):
                stripped = line.strip()
                if not stripped or stripped.startswith("#"):
                    continue

                if '=' not in stripped:
                    raise ConfigError(f"Invalid syntax at line "
                                      f"{line_number}: '{line}'")

                key, value = stripped.split("=", 1)
                raw_dict[key.strip()] = value.strip()
    except FileNotFoundError as exc:
        raise ConfigError(f"Config file not found {path}") from exc

    return raw_dict


def _parse_coordinates(value: str, field_name: str) -> Tuple[int, int]:
    """Read the config file and return a Tuple of coordinates"""

    try:
        x_value, y_value = value.split(",")
        return int(x_value), int(y_value)
    except ValueError as exc:
        raise ConfigError(f"Invalid coordinates "
                          f"for {field_name}: '{value}'") from exc


def _parse_perfection(value: str) -> bool:
    """Read the config file and return a Tuple of coordinates"""

    if value.strip().lower() in ("yes", "1", "true"):
        return True
    elif value.strip().lower() in ("no", "0", "false"):
        return False
    else:
        raise ConfigError(f"{value} is an invalid format for boolean")


def _perse_seed(value: str) -> int:
    """Read the config file and return a int value"""

    seed: int
    try:
        seed = int(value)
    except ValueError as exc:
        raise ConfigError("Seed must be a integer") from exc
    return seed


def parse_config(path: str) -> MazeConfig:
    """Parse and validate a maze configuration file.
    Args:
        path: Path to the configuration file.
    Returns:
        A validated MazeConfig instance.
    Raises:
        ConfigError: If the file is missing, malformed, or logically invalid.
    """

    config_path = Path(path)
    read_lines = _read_raw_lines(config_path)
    missing_keys = REQUIRED_KEYS - read_lines.keys()

    if missing_keys:
        raise ConfigError(f"Missing required key(s) "
                          f"{', '.join(sorted(missing_keys))}")

    try:
        width = int(read_lines["WIDTH"])
        height = int(read_lines["HEIGHT"])
    except ValueError as exc:
        raise ConfigError("WIDTH and HEIGHT must be integers.") from exc

    if width <= 0 or height <= 0:
        raise ConfigError("WIDTH and HEIGHT must be positive integers "
                          "and greater than zero.")

    entry = _parse_coordinates(read_lines["ENTRY"], "ENTRY")
    exit = _parse_coordinates(read_lines["EXIT"], "EXIT")

    for name, (x, y) in (("ENTRY", entry), ("EXIT", exit)):
        if (x < 0 or y < 0):
            raise ConfigError(f"{name} {x, y} must not be negative.")
        if not (0 <= x < width and 0 <= y < height):
            raise ConfigError(f"{name} {x, y} are out of bounds")

    if entry == exit:
        raise ConfigError("Coordinates 'entry' and 'exit' must be different")

    perfect = _parse_perfection(read_lines["PERFECT"])

    output_file = str(read_lines["OUTPUT_FILE"])

    if "SEED" not in read_lines:
        seed = None
    else:
        seed = _perse_seed(read_lines["SEED"])

    return MazeConfig(
        width=width,
        height=height,
        entry=entry,
        exit=exit,
        perfect=perfect,
        output_file=output_file,
        seed=seed)
