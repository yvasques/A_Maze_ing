from dataclasses import dataclass
from pathlib import Path


@dataclass
class MazeConfig:
    width:int
    heght:int
    entry:tuple[int, int]
    exit:tuple[int, int]
    output_file: str
    perfect: bool
    seed: int






def parse_config(Path: str) -> MazeConfig:
    return MazeConfig(
		width=width,
		heght=heght,
		entry= entry,
		exit=exit,
		output_file=output_file,
		perfect=perfect,
		seed=seed
	)
