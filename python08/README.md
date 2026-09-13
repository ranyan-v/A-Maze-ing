*This project has been created as part of the 42 curriculum by rayan, rjiao.*

# Description
A-Maze_Ing is a complete maze generation, braiding, solving, and interactive visualization toolkit.

# Instructions

## Reusable Library: `mazegen`

The core generation and solving mechanics are packaged into the standalone `mazegen` module.

### Installation
pip install build
python3 -m build --wheel --outdir .

Install the prebuilt wheel directly via `pip`:

pip install mazegen-1.0.0-py3-none-any.whl

### Usage example:
from mazegen import MazeGenerator, shortest_path

#### Generate a Pac-Man braided maze with 42 mask
generator = MazeGenerator(
    width=15,
    height=15,
    entry=(0, 0),
    exit=(14, 14),
    seed=42,
    perfect=False,
)
maze = generator.generate()

#### Solve shortest path
path = shortest_path(maze)
print("Solution steps:", path)

#### Export hex rows
for row in maze.hexadecimal_rows():
    print(row)

# Team management
## The roles of each team member
rayan is responsible for the mathematical model and algorithm implementation, including the maze data structure design, open space prevention, BFS based shortest path solver, etc.

rjiao works on issues other than maze generators, i.e. the outer workspace, e.g. the validationg of configuration file, the visualization of the maze and solver, and packaging of project.

## Anticipation and realisation
After reading and understanding the subject file together, we divided the work as mentioned before, and started working independently. But we soon realized that a lot of the parts are highly related, or even a bit ambigious. So in the end we cooperate even more than expected.

Along with the progress of other python modules, we ontice that it would have been better if we had more knowledge in Python, like the package management system in module 08, and it would be helpful.

For this project, we use tools like python 3.10+, flake8, mypy, poetry.

# Resources

