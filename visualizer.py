"""Terminal ASCII/ANSI interactive visualization for maze instances."""

import os
from collections.abc import Callable
from dataclasses import dataclass
from typing import TypeAlias

from mazegen.maze import DIRECTION_DELTAS, Direction, Maze, Position
from mazegen.solver import Solution

ColorPalette: TypeAlias = tuple[str, ...]

WALL_COLORS: ColorPalette = (
    "\033[97m",  # 白色
    "\033[94m",  # 蓝色
    "\033[96m",  # 青色
    "\033[95m",  # 洋红色
    "\033[33m",  # 暗黄色
)

PATTERN_42_COLORS: ColorPalette = (
    "\033[90m",  # 灰色
    "\033[35m",  # 暗紫色
    "\033[31m",  # 暗红色
    "\033[32m",  # 暗绿色
)

COLOR_RESET = "\033[0m"
COLOR_ENTRY = "\033[92m"      # 亮绿色
COLOR_EXIT = "\033[91m"       # 亮红色
COLOR_PATH = "\033[93m"       # 亮黄色


@dataclass
class VisualizerState:
    """Stores the current visualizer display settings."""

    show_path: bool = True
    wall_color_idx: int = 0
    pattern_color_idx: int = 0


def _decode_solution_positions(
    entry: Position,
    solution: Solution,
) -> set[Position]:
    """Convert a solution string ('NEE...')
    into a set of visited coordinates."""
    dir_map = {d.value: d for d in Direction}
    path_positions: set[Position] = set()
    cur_x, cur_y = entry

    for step in solution:
        direction = dir_map.get(step)
        if direction:
            dx, dy = DIRECTION_DELTAS[direction]
            cur_x += dx
            cur_y += dy
            path_positions.add((cur_x, cur_y))

    return path_positions


def render_maze(
    maze: Maze,
    solution: Solution = "",
    state: VisualizerState | None = None,
) -> str:
    if state is None:
        state = VisualizerState()

    path_positions = (
        _decode_solution_positions(maze.entry, solution)
        if state.show_path
        else set()
    )

    wall_color = WALL_COLORS[state.wall_color_idx]
    pattern_color = PATTERN_42_COLORS[state.pattern_color_idx]
    lines: list[str] = []
    # “双行展开法”（Two-Row Expansion per Grid Row）：对于迷宫的每一行 y，
    # 都分解为顶部水平墙壁行和房间主体垂直墙壁行两行来打印。
    for y in range(maze.height):
        # 1. 顶部北墙
        top_parts: list[str] = []
        for x in range(maze.width):
            top_parts.append(f"{wall_color}+{COLOR_RESET}")
            if not maze.is_open((x, y), Direction.NORTH):
                top_parts.append(f"{wall_color}---{COLOR_RESET}")
            else:
                top_parts.append("   ")
        top_parts.append(f"{wall_color}+{COLOR_RESET}")
        lines.append("".join(top_parts))

        # 2. 房间内部与西墙
        mid_parts: list[str] = []
        for x in range(maze.width):
            pos: Position = (x, y)
            if not maze.is_open(pos, Direction.WEST):
                mid_parts.append(f"{wall_color}|{COLOR_RESET}")
            else:
                mid_parts.append(" ")

            if pos == maze.entry:
                mid_parts.append(f"{COLOR_ENTRY} S {COLOR_RESET}")
            elif pos == maze.exit:
                mid_parts.append(f"{COLOR_EXIT} E {COLOR_RESET}")
            elif maze.cell(pos).walls == 0xF:
                mid_parts.append(f"{pattern_color}███{COLOR_RESET}")
            elif pos in path_positions:
                mid_parts.append(f"{COLOR_PATH} • {COLOR_RESET}")
            else:
                mid_parts.append("   ")

        last_pos: Position = (maze.width - 1, y)
        if not maze.is_open(last_pos, Direction.EAST):
            mid_parts.append(f"{wall_color}|{COLOR_RESET}")
        else:
            mid_parts.append(" ")
        lines.append("".join(mid_parts))

    # 3. 最底部南墙
    bot_parts: list[str] = []
    for x in range(maze.width):
        bot_parts.append(f"{wall_color}+{COLOR_RESET}")
        last_row_pos: Position = (x, maze.height - 1)
        if not maze.is_open(last_row_pos, Direction.SOUTH):
            bot_parts.append(f"{wall_color}---{COLOR_RESET}")
        else:
            bot_parts.append("   ")
    bot_parts.append(f"{wall_color}+{COLOR_RESET}")
    lines.append("".join(bot_parts))

    return "\n".join(lines)


def display_maze(
    maze: Maze,
    solution: Solution = "",
    state: VisualizerState | None = None,
) -> None:
    """Print the rendered maze to the terminal."""
    print(render_maze(maze, solution, state))


def interactive_loop(
    initial_maze: Maze,
    initial_solution: Solution,
    regenerate_fn: Callable[[], tuple[Maze, Solution]],
) -> None:
    """Start the interactive terminal CLI loop."""
    current_maze = initial_maze
    current_solution = initial_solution
    state = VisualizerState()

    while True:
        # 清屏保证画面固定在终端最上方
        os.system("clear" if os.name == "posix" else "cls")

        print("=== A-Maze-Ing Terminal Visualizer ===")
        display_maze(current_maze, current_solution, state)
        print("\nControls:")
        print(" [r] Re-generate new maze")
        print(f" [p] Display shortest path (Currently: \
{'ON' if state.show_path else 'OFF'})")
        print(f" [c] Change wall colour (Current index: \
{state.wall_color_idx + 1}/{len(WALL_COLORS)})")
        print(f" [4] Change '42' pattern colour (Current index: \
{state.pattern_color_idx + 1}/{len(PATTERN_42_COLORS)})")
        print(" [q] Quit visualizer")

        try:
            cmd = input("\nSelect an action: ").strip().lower()
        except (KeyboardInterrupt, EOFError):
            print("\nExiting visualizer.")
            break

        if cmd == "q":
            break
        elif cmd == "r":
            current_maze, current_solution = regenerate_fn()
        elif cmd == "p":
            state.show_path = not state.show_path
        elif cmd == "c":
            state.wall_color_idx = (state.wall_color_idx + 1) % \
                len(WALL_COLORS)
        elif cmd == "4":
            state.pattern_color_idx = (
                state.pattern_color_idx + 1
            ) % len(PATTERN_42_COLORS)
