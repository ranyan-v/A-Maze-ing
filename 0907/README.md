# A-Maze-Ing

A complete maze generation, braiding, solving, and interactive visualization toolkit.

## Reusable Library: `mazegen`

The core generation and solving mechanics are packaged into the standalone `mazegen` module.

### Installation
pip install build
python3 -m build --wheel --outdir .

Install the prebuilt wheel directly via `pip`:

```bash
pip install mazegen-1.0.0-py3-none-any.whl

### Usage example:
from mazegen import MazeGenerator, shortest_path

# Generate a Pac-Man braided maze with 42 mask
generator = MazeGenerator(
    width=15,
    height=15,
    entry=(0, 0),
    exit=(14, 14),
    seed=42,
    perfect=False,
)
maze = generator.generate()

# Solve shortest path
path = shortest_path(maze)
print("Solution steps:", path)

# Export hex rows
for row in maze.hexadecimal_rows():
    print(row)