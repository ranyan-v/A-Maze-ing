"""Perfect maze generation."""

import random

from errors import GenerationError
from maze import Maze, Position
from pattern import reserved_cells


class MazeGenerator:
    """Generate a perfect maze using randomized depth-first search."""

    def __init__(
        self,
        width: int,
        height: int,
        entry: Position,
        exit: Position,
        seed: int | None = None,
    ) -> None:
        self.width = width
        self.height = height
        self.entry = entry
        self.exit = exit
        self._random = random.Random(seed)

    def generate(self) -> Maze:
        """Generate and return a connected, loop-free maze."""

        maze = Maze(self.width, self.height, self.entry, self.exit)
        reserved = reserved_cells(self.width, self.height)
        if self.entry in reserved or self.exit in reserved:
            raise GenerationError(
                "entry and exit cannot be reserved pattern cells"
            )

        expected_cells = self.width * self.height - len(reserved)
        visited: set[Position] = {self.entry}
        stack: list[Position] = [self.entry]

        while stack:
            current = stack[-1]
            candidates = [
                (position, direction)
                for position, direction in maze.neighbours(current)
                if position not in visited and position not in reserved
            ]

            if not candidates:
                stack.pop()
                continue

            next_position, _ = self._random.choice(candidates)
            maze.carve(current, next_position)
            visited.add(next_position)
            stack.append(next_position)

        if len(visited) != expected_cells:
            raise GenerationError("could not connect every maze cell")
        return maze
