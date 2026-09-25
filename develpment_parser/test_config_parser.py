# test_config_parser.py
try:
	import pytest
except ImportError as err:
    print(err)
from develpment_parser.config_parser import *


def write_config(tmp_path, content: str) -> str:
    """Helper to create a temporary config file and return its path."""
    config_file = tmp_path / "config.txt"
    config_file.write_text(content, encoding="utf-8")
    return str(config_file)


def test_valid_config(tmp_path):
    content = (
        "WIDTH=20\n"
        "HEIGHT=15\n"
        "ENTRY=0,0\n"
        "EXIT=19,14\n"
        "OUTPUT_FILE=maze.txt\n"
        "PERFECT=True\n"
    )
    path = write_config(tmp_path, content)

    config = parse_config(path)

    assert isinstance(config, MazeConfig)
    assert config.width == 20
    assert config.height == 15
    assert config.entry == (0, 0)
    assert config.exit == (19, 14)
    assert config.perfect is True


def test_missing_key_raises_error(tmp_path):
    content = "WIDTH=20\nHEIGHT=15\n"  # faltam ENTRY, EXIT, etc.
    path = write_config(tmp_path, content)

    with pytest.raises(ConfigError, match="Missing required key"):
        parse_config(path)


def test_invalid_syntax_raises_error(tmp_path):
    content = "WIDTH 20\n"  # sem "="
    path = write_config(tmp_path, content)

    with pytest.raises(ConfigError, match="Invalid syntax"):
        parse_config(path)


def test_entry_equals_exit_raises_error(tmp_path):
    content = (
        "WIDTH=10\n"
        "HEIGHT=10\n"
        "ENTRY=0,0\n"
        "EXIT=0,0\n"
        "OUTPUT_FILE=maze.txt\n"
        "PERFECT=True\n"
    )
    path = write_config(tmp_path, content)

    with pytest.raises(ConfigError, match="must be different"):
        parse_config(path)


def test_out_of_bounds_entry_raises_error(tmp_path):
    content = (
        "WIDTH=5\n"
        "HEIGHT=5\n"
        "ENTRY=10,10\n"
        "EXIT=1,1\n"
        "OUTPUT_FILE=maze.txt\n"
        "PERFECT=True\n"
    )
    path = write_config(tmp_path, content)

    with pytest.raises(ConfigError, match="out of bounds"):
        parse_config(path)


def test_comments_and_blank_lines_are_ignored(tmp_path):
    content = (
        "# this is a comment\n"
        "\n"
        "WIDTH=8\n"
        "HEIGHT=8\n"
        "ENTRY=0,0\n"
        "EXIT=7,7\n"
        "OUTPUT_FILE=maze.txt\n"
        "PERFECT=False\n"
    )
    path = write_config(tmp_path, content)

    config = parse_config(path)

    assert config.width == 8
    assert config.perfect is False


def test_file_not_found_raises_error():
    with pytest.raises(ConfigError, match="not found"):
        parse_config("non_existent_file.txt")
