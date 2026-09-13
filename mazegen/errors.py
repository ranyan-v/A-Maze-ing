"""Exceptions raised by the A-Maze-ing application."""


class MazeError(Exception):
    """Base class for expected application errors."""


class ConfigError(MazeError):
    """Raised when a configuration file is invalid or cannot be read."""


class GenerationError(MazeError):
    """Raised when a maze cannot be generated."""


class SolveError(MazeError):
    """Raised when a maze has no solution."""


class OutputError(MazeError):
    """Raised when the generated maze cannot be written."""
