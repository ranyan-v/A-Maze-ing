"""Core maze and cell data structures."""

from dataclasses import dataclass
from enum import Enum
from typing import Iterator, TypeAlias

from errors import MazeError

Position: TypeAlias = tuple[int, int]


class Direction(Enum):
    """A cardinal direction and its output representation."""

    NORTH = "N"
    EAST = "E"
    SOUTH = "S"
    WEST = "W"


DIRECTION_DELTAS: dict[Direction, tuple[int, int]] = {
    Direction.NORTH: (0, -1),
    Direction.EAST: (1, 0),
    Direction.SOUTH: (0, 1),
    Direction.WEST: (-1, 0),
}

WALL_BITS: dict[Direction, int] = {
    Direction.NORTH: 0x1,
    Direction.EAST: 0x2,
    Direction.SOUTH: 0x4,
    Direction.WEST: 0x8,
}

OPPOSITE: dict[Direction, Direction] = {
    Direction.NORTH: Direction.SOUTH,
    Direction.EAST: Direction.WEST,
    Direction.SOUTH: Direction.NORTH,
    Direction.WEST: Direction.EAST,
}


@dataclass
class Cell:
    """A maze cell represented by a four-bit wall mask."""

    walls: int = 0xF


class Maze:
    """Mutable maze data model shared by generation, solving, and output."""

    def __init__(
        self,
        width: int,
        height: int,
        entry: Position,
        exit: Position,
    ) -> None:
        if width <= 0 or height <= 0:
            raise MazeError("maze width and height must be positive")
        if entry == exit:
            raise MazeError("entry and exit must be different")

        self.width = width
        self.height = height
        self.entry = entry
        self.exit = exit
        self.cells: list[list[Cell]] = [
            [Cell() for _ in range(width)] for _ in range(height)
        ]

        self._validate_position(entry, "entry")
        self._validate_position(exit, "exit")

    def cell(self, position: Position) -> Cell:
        """Return the cell at ``position``."""

        self._validate_position(position, "cell")
        x, y = position
        return self.cells[y][x]

    def neighbours(
        self,
        position: Position,
    ) -> Iterator[tuple[Position, Direction]]:
        """Yield in-bounds neighbouring positions and their directions."""

        self._validate_position(position, "cell")
        x, y = position
        for direction, (dx, dy) in DIRECTION_DELTAS.items():
            neighbour = (x + dx, y + dy)
            if self.in_bounds(neighbour):
                yield neighbour, direction

    def in_bounds(self, position: Position) -> bool:
        """Return whether ``position`` is inside the maze."""

        x, y = position
        return 0 <= x < self.width and 0 <= y < self.height

    def is_open(self, position: Position, direction: Direction) -> bool:
        """Return whether the wall in ``direction`` is open."""

        return not self.cell(position).walls & WALL_BITS[direction]

    def carve(self, first: Position, second: Position) -> None:
        """Open the shared wall between two orthogonally adjacent cells."""

        self._validate_position(first, "first cell")
        self._validate_position(second, "second cell")

        direction = self._direction_between(first, second)
        opposite = OPPOSITE[direction]
        self.cell(first).walls &= ~WALL_BITS[direction]
        self.cell(second).walls &= ~WALL_BITS[opposite]

    def hexadecimal_rows(self) -> list[str]:
        """Return the maze rows encoded as uppercase hexadecimal digits."""

        return [
            "".join(format(cell.walls, "X") for cell in row)
            for row in self.cells
        ]

    def _validate_position(self, position: Position, label: str) -> None:
        if not self.in_bounds(position):
            raise MazeError(
                f"{label} position is outside the maze: {position}"
            )

    @staticmethod
    def _direction_between(
        first: Position,
        second: Position,
    ) -> Direction:
        dx = second[0] - first[0]
        dy = second[1] - first[1]
        for direction, delta in DIRECTION_DELTAS.items():
            if (dx, dy) == delta:
                return direction
        raise MazeError("cells must be orthogonally adjacent")
