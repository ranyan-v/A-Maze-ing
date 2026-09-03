"""Command-line entry point for the A-Maze-ing Phase 1 MVP."""

import sys
from collections.abc import Sequence

from config import Config
from errors import ConfigError, MazeError
from generator import MazeGenerator
from output import write_output
from solver import shortest_path


def main(arguments: Sequence[str] | None = None) -> int:
    """Run the Phase 1 pipeline and return a process exit code."""

    args = list(sys.argv[1:] if arguments is None else arguments)
    if len(args) != 1:
        print("Usage: python3 a_maze_ing.py config.txt", file=sys.stderr)
        return 2

    try:
        config = Config.from_file(args[0])
        if not config.perfect:
            raise ConfigError(
                "PERFECT=False is not implemented in Phase 1"
            )

        maze = MazeGenerator(
            width=config.width,
            height=config.height,
            entry=config.entry,
            exit=config.exit,
            seed=config.seed,
        ).generate()
        solution = shortest_path(maze)
        write_output(config.output_file, maze, solution)
    except MazeError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    except Exception as exc:  # pragma: no cover - last-resort CLI safety net
        print(f"Error: unexpected failure: {exc}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
