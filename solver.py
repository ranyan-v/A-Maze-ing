"""Shortest-path solving for maze instances."""

from collections import deque
from typing import TypeAlias

from errors import SolveError
from maze import Direction, Maze, Position

Solution: TypeAlias = str


def shortest_path(maze: Maze) -> Solution:
    """Return a shortest path from the maze entry to its exit using BFS."""

    queue: deque[Position] = deque([maze.entry])
    parents: dict[Position, tuple[Position, Direction] | None] = {
        maze.entry: None
    }

    while queue:
        current = queue.popleft()
        if current == maze.exit:
            break

        for neighbour, direction in maze.neighbours(current):
            if not maze.is_open(current, direction):
                continue
            if neighbour in parents:
                continue
            parents[neighbour] = (current, direction)
            queue.append(neighbour)

    if maze.exit not in parents:
        raise SolveError("no path exists from entry to exit")

    steps: list[str] = []
    current = maze.exit
    while current != maze.entry:
        parent = parents[current]
        if parent is None:
            raise SolveError("could not reconstruct the shortest path")
        previous, direction = parent
        steps.append(direction.value)
        current = previous

    steps.reverse()
    return "".join(steps)
