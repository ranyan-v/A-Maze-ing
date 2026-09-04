"""Minimal Phase 1 tests."""

import tempfile
import unittest
from pathlib import Path

from config import Config
from errors import ConfigError, MazeError
from generator import MazeGenerator
from maze import Direction, Maze
from output import write_output
from solver import shortest_path


class ConfigTests(unittest.TestCase):
    def test_valid_configuration(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            filename = Path(directory) / "config.txt"
            filename.write_text(
                "WIDTH=4\n"
                "HEIGHT=3\n"
                "ENTRY=0,0\n"
                "EXIT=3,2\n"
                "OUTPUT_FILE=maze.txt\n"
                "PERFECT=True\n"
                "SEED=7\n",
                encoding="utf-8",
            )
            config = Config.from_file(str(filename))

        self.assertEqual(config.width, 4)
        self.assertEqual(config.height, 3)
        self.assertEqual(config.entry, (0, 0))
        self.assertEqual(config.exit, (3, 2))
        self.assertEqual(config.seed, 7)

    def test_invalid_configuration_is_reported(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            filename = Path(directory) / "config.txt"
            filename.write_text("WIDTH=0\n", encoding="utf-8")
            with self.assertRaises(ConfigError):
                Config.from_file(str(filename))


class MazeTests(unittest.TestCase):
    def test_carving_updates_both_shared_walls(self) -> None:
        maze = Maze(2, 2, (0, 0), (1, 1))
        maze.carve((0, 0), (1, 0))

        self.assertTrue(maze.is_open((0, 0), Direction.EAST))
        self.assertTrue(maze.is_open((1, 0), Direction.WEST))
        self.assertEqual(maze.hexadecimal_rows()[0], "D7")

    def test_carving_non_adjacent_cells_fails(self) -> None:
        maze = Maze(2, 2, (0, 0), (1, 1))
        with self.assertRaises(MazeError):
            maze.carve((0, 0), (1, 1))


class GeneratorTests(unittest.TestCase):
    def test_seed_reproduces_the_same_maze(self) -> None:
        arguments = (8, 6, (0, 0), (7, 5))
        first = MazeGenerator(*arguments, seed=123).generate()
        second = MazeGenerator(*arguments, seed=123).generate()
        self.assertEqual(first.hexadecimal_rows(), second.hexadecimal_rows())

    def test_generated_maze_is_connected_and_loop_free(self) -> None:
        maze = MazeGenerator(8, 6, (0, 0), (7, 5), seed=123).generate()
        visited = {maze.entry}
        pending = [maze.entry]
        edges = 0

        while pending:
            current = pending.pop()
            for neighbour, direction in maze.neighbours(current):
                if not maze.is_open(current, direction):
                    continue
                if current[0] < neighbour[0] or current[1] < neighbour[1]:
                    edges += 1
                if neighbour not in visited:
                    visited.add(neighbour)
                    pending.append(neighbour)

        self.assertEqual(len(visited), maze.width * maze.height)
        self.assertEqual(edges, maze.width * maze.height - 1)


class SolverTests(unittest.TestCase):
    def test_solver_returns_a_shortest_valid_path(self) -> None:
        maze = Maze(2, 2, (0, 0), (0, 1))
        maze.carve((0, 0), (1, 0))
        maze.carve((1, 0), (1, 1))
        maze.carve((1, 1), (0, 1))

        self.assertEqual(shortest_path(maze), "ESW")


class OutputTests(unittest.TestCase):
    def test_output_has_required_sections_and_newlines(self) -> None:
        maze = Maze(1, 2, (0, 0), (0, 1))
        maze.carve((0, 0), (0, 1))

        with tempfile.TemporaryDirectory() as directory:
            filename = Path(directory) / "maze.txt"
            write_output(filename, maze, shortest_path(maze))
            contents = filename.read_text(encoding="ascii")

        self.assertEqual(contents, "B\nE\n\n0,0\n0,1\nS\n")


if __name__ == "__main__":
    unittest.main()
