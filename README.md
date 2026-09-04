# A-Maze-ing

Phase 1 currently provides configuration parsing, perfect-maze generation,
shortest-path solving, and the required output file.

## Run

```bash
python3 a_maze_ing.py config.txt
```

The configuration file must be the only command-line argument.

## Test

```bash
python3 -m unittest discover -s tests -v
```

The `42` pattern, playable mazes, visualization, reusable packaging, and
bonus features are intentionally not implemented yet.
