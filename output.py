"""Writing the required maze output format."""

from pathlib import Path

from errors import OutputError
from maze import Maze
from solver import Solution


def write_output(filename: Path, maze: Maze, solution: Solution) -> None:
    """Write the maze, coordinates, and solution to ``filename``."""

    entry_x, entry_y = maze.entry
    exit_x, exit_y = maze.exit
    lines = maze.hexadecimal_rows()
    lines.extend(
        [
            "",
            f"{entry_x},{entry_y}",
            f"{exit_x},{exit_y}",
            solution,
        ]
    )

    try:
        filename.write_text("\n".join(lines) + "\n", encoding="ascii")
    except OSError as exc:
        raise OutputError(
            f"cannot write output file '{filename}': {exc}"
        ) from exc
