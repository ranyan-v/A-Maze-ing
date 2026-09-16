"""Maze generation supporting both Perfect and Pac-Man modes."""

import random

from mazegen.errors import GenerationError
from mazegen.maze import Direction, Maze, Position
from mazegen.pattern import reserved_cells


class MazeGenerator:
    """Generate a maze using DFS spanning trees and optional braiding."""

    def __init__(
        self,
        width: int,
        height: int,
        entry: Position,
        exit: Position,
        seed: int | None = None,
        perfect: bool = True,
    ) -> None:
        self.width = width
        self.height = height
        self.entry = entry
        self.exit = exit
        self.perfect = perfect
        self._random = random.Random(seed)

    def _is_open_3x3(self, maze: Maze, left_x: int, top_y: int) -> bool:
        """Return True if all 12 interior walls
            within the 3x3 window are open."""

        # 1. 检查 6 道内部横向共用墙 (x 到 x+1)
        for dy in range(3):  # <-- 检查三行
            y = top_y + dy
            for dx in range(2):  # <-- 检查每行的两道墙
                x = left_x + dx
                if not maze.is_open((x, y), Direction.EAST):  # <-- 检查所在位置往东走
                    return False

        # 2. 检查 6 道内部纵向共用墙 (y 到 y+1)
        for dy in range(2):
            y = top_y + dy
            for dx in range(3):
                x = left_x + dx
                if not maze.is_open((x, y), Direction.SOUTH):
                    return False

        return True

    def _generate_spanning_tree(
        self,
        maze: Maze,
        reserved: frozenset[Position],
    ) -> None:
        expected_cells = self.width * self.height - len(reserved)  # <-- 该访问数量
        visited: set[Position] = {self.entry}  # <-- 存储：已经访问过的 cell
        stack: list[Position] = [self.entry]  # <-- 记录最后一个可行位置

        while stack:  # <-- 只要 stack 里面还有东西，就继续 DFS
            current = stack[-1]  # <-- 取 stack 最后一个元素
            candidates = [
                (position, direction)
                for position, direction in maze.neighbours(current)
                if position not in visited and position not in reserved
            ]  # <-- Unvisited and non-reserved neighboring cells

            if not candidates:  # <-- 没路了，回溯
                stack.pop()
                continue  # <-- 结束这一轮 while，直接进入下一轮

            next_position, _ = self._random.choice(candidates)  # <-- 要第一个
            maze.carve(current, next_position)
            visited.add(next_position)
            stack.append(next_position)

        if len(visited) != expected_cells:  # <-- 实际访问数量是不是理论上应该访问的数量
            raise GenerationError("could not connect every maze cell")

    def _has_open_3x3(self, maze: Maze) -> bool:
        """Return True if the maze contains any open 3x3 area."""

        if self.width < 3 or self.height < 3:
            return False

        for top_y in range(self.height - 2):
            for left_x in range(self.width - 2):
                if self._is_open_3x3(maze, left_x, top_y):
                    return True

        return False

    def _add_loops(
        self,
        maze: Maze,
        reserved: frozenset[Position],
        extra_loops_target: int = 5
    ) -> int:
        """Add extra connections without creating 3x3 open areas."""

        candidates: list[tuple[Position, Position]] = []

        for y in range(self.height):
            for x in range(self.width):
                cur: Position = (x, y)
                if cur in reserved:
                    continue
                # 仅向东、南方向收集封闭内墙，避免重复收集同一面墙
                for direction in (Direction.EAST, Direction.SOUTH):
                    for neighbour, dir_to_nbr in maze.neighbours(cur):
                        if (
                            dir_to_nbr == direction
                            and neighbour not in reserved
                            and not maze.is_open(cur, direction)
                        ):
                            candidates.append((cur, neighbour))

        self._random.shuffle(candidates)

        loops_added = 0
        # 打通若干道内墙增加独立回路
        for first, second in candidates:
            if loops_added >= extra_loops_target:
                break
            # Try opening the wall.
            maze.carve(first, second)

            # If it creates a 3x3 open area, undo it.
            if self._has_open_3x3(maze):
                maze.seal(first, second)
                continue

            loops_added += 1

        return loops_added

    def _count_open_walls(self, maze: Maze, position: Position) -> int:
        """计算某个格子四周打开了多少面墙。"""
        return sum(
            1 for _, direction in maze.neighbours(position)
            if maze.is_open(position, direction)
        )

    def _braid_dead_ends(
        self,
        maze: Maze,
        reserved: frozenset[Position],
    ) -> int:
        """编织消除死胡同：对只有 1 面墙开着的非 42 格子，随机打通另一面内墙。"""
        # 最多循环迭代几次，直到死胡同完全消除
        edges_added = 0
        for _ in range(5):
            dead_ends: list[Position] = []
            for y in range(self.height):
                for x in range(self.width):
                    pos: Position = (x, y)
                    if pos in reserved:
                        continue
                    # 只有 1 面墙是开着的格子即为死胡同
                    if self._count_open_walls(maze, pos) == 1:
                        dead_ends.append(pos)

            if not dead_ends:
                break

            self._random.shuffle(dead_ends)
            for pos in dead_ends:
                if self._count_open_walls(maze, pos) != 1:
                    continue  # 可能已经被邻居打通过了，跳过

                # 寻找四周未打通的、合法的普通房间邻居（排除 42 和越界）
                carve_candidates = [
                    neighbour
                    for neighbour, direction in maze.neighbours(pos)
                    if (
                        neighbour not in reserved
                        and not maze.is_open(pos, direction)
                    )
                ]

                self._random.shuffle(carve_candidates)

                for chosen in carve_candidates:
                    maze.carve(pos, chosen)

                    if self._has_open_3x3(maze):
                        maze.seal(pos, chosen)
                        continue

                    edges_added += 1
                    break
        return edges_added

    def generate(self) -> Maze:
        """Generate and return a valid maze according to configuration."""

        maze = Maze(self.width, self.height, self.entry, self.exit)
        reserved = reserved_cells(self.width, self.height)
        if self.entry in reserved or self.exit in reserved:
            raise GenerationError(
                "entry and exit cannot be reserved pattern cells"
            )

        # 1. 生成基础生成树 (DFS)
        self._generate_spanning_tree(maze, reserved)

        # 2. 若为 Pac-Man 模式，增加回路、消除死胡同并防止 3x3 大开阔区
        if not self.perfect:
            loops_added = self._add_loops(maze, reserved)
            loops_added += self._braid_dead_ends(maze, reserved)

        if not self.perfect and loops_added < 2:
            raise GenerationError(
                "could not create at least two loops"
            )

        return maze
