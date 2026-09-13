"""Reusable Maze Generation and Solving Library."""

from mazegen.errors import GenerationError, MazeError, SolveError
from mazegen.generator import MazeGenerator
from mazegen.maze import Direction, Maze, Position
from mazegen.solver import shortest_path

__version__ = "1.0.0"
__all__ = [
    "Maze",
    "MazeGenerator",
    "Direction",
    "Position",
    "shortest_path",
    "MazeError",
    "GenerationError",
    "SolveError",
]
