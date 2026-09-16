*This project has been created as part of the 42 curriculum by rayan, rjiao.*

# Description
A-Maze_Ing is a complete maze generation, braiding, solving, and interactive visualization toolkit.
DFS (Depth-first search) is used to generate the maze, because it  only tracks the current branch on the stack in the worst case, but typically far fewer cells in memory at any one time, making it lightweight and fast to execute.

BFS (Breadth-first search) is used to find the solution  because its ersult is mathematically guaranteed to be the shortest path.

We used Terminal ASCII renddering.

# Instructions
## Configuration
The configuration file uses:
KEY=VALUE
Lines beginning with # are comments and must be ignored.
The following parameters are mandatory:

WIDTH
HEIGHT
ENTRY
EXIT
OUTPUT_FILE
PERFECT
Additional parameters may be supported.
For example:
WIDTH=20
HEIGHT=15
ENTRY=0,0
EXIT=19,14
OUTPUT_FILE=maze.txt
PERFECT=True
The program must validate configuration values and handle invalid configuration gracefully.
Invalid configurations must produce a clear error message instead of an unexpected crash.

## compile

python3 a_maze_ing.py config.txt

python3 maze_analyzer.py maze.txt

## Reusable Library: `mazegen`
The maze-generation logic is reusable independently from the main application.
It is provided as a standalone module.
The reusable part contains one unique maze-generator class, for example:
MazeGenerator
The generator is importable by another Python program;
allow custom parameters such as maze size and seed;
provide access to the generated maze structure;
provide access to at least one solution.

The core generation and solving mechanics are packaged into the standalone `mazegen` module.

### Installation
pip install build

python3 -m build --wheel --outdir .

### Create a new virtual environment to test
python -m venv test 

source test/bin/activate

pip install mazegen-0.1.0-py3-none-any.whl

deactivate
# Team management
## The roles of each team member
rayan is responsible for the mathematical model and algorithm implementation, including the maze data structure design, open space prevention, BFS based shortest path solver, etc.

rjiao works on issues other than maze generators, i.e. the outer workspace, e.g. the validationg of configuration file, the visualization of the maze and solver, and packaging of project.

## Anticipation and realisation
After reading and understanding the subject file together, we divided the work as mentioned before, and started working independently. But we soon realized that a lot of the parts are highly related, or even a bit ambigious. So in the end we cooperate even more than expected.

Along with the progress of other python modules, we notice that it would have been better if we had more knowledge in Python, like the package management system in module 08, and it would be helpful.

For this project, we use tools like python 3.10+, flake8, mypy, poetry.

# Resources
We used AI mainly to get better understanding of the concepts of different kinds of maze, the process of maze generating, as well as the visualization process.
