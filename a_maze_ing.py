"""Command-line entry point for the A-Maze-ing application."""

import sys
from collections.abc import Sequence

from config import Config
from mazegen.errors import MazeError
from mazegen.maze import Maze
from mazegen.generator import MazeGenerator
from output import write_output
from mazegen.solver import shortest_path
from visualizer import interactive_loop


def main(arguments: Sequence[str] | None = None) -> int:
    """Run the pipeline and launch interactive terminal visualizer."""

    args = list(sys.argv[1:] if arguments is None else arguments)
    if len(args) != 1:
        print("Usage: python3 a_maze_ing.py config.txt", file=sys.stderr)
        return 2

    try:
        config = Config.from_file(args[0])

        def generate_and_solve() -> tuple[Maze, str]:
            # 重新生成时不强制锁定 seed，产生真正的新随机迷宫
            new_maze = MazeGenerator(
                width=config.width,
                height=config.height,
                entry=config.entry,
                exit=config.exit,
                seed=None,
                perfect=config.perfect,
            ).generate()
            new_solution = shortest_path(new_maze)
            return new_maze, new_solution

        # 首次生成使用配置文件自带的 seed（若有定义）
        maze = MazeGenerator(
            width=config.width,
            height=config.height,
            entry=config.entry,
            exit=config.exit,
            seed=config.seed,
            perfect=config.perfect,
        ).generate()
        solution = shortest_path(maze)

        # 按照题目规范，写出第一份迷宫到输出文件
        write_output(config.output_file, maze, solution)
        print(f"Initial maze successfully saved to {config.output_file}.")

        # 启动交互式可视化
        interactive_loop(maze, solution, generate_and_solve)

    except MazeError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    except Exception as exc:  # pragma: no cover
        print(f"Error: unexpected failure: {exc}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
