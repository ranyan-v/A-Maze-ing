# A-Maze-ing — Requirements

## 1. Project Overview

The project must generate a maze from a configuration file, save the
generated maze in the required hexadecimal format, calculate a valid
shortest path between the entry and exit, and provide an interactive
visual representation.

The project must also provide a reusable maze-generation module.

---

## 2. Program Entry Point

The main program must be:

    a_maze_ing.py

It must be executable with:

    python3 a_maze_ing.py config.txt

The configuration file is the only command-line argument.

The configuration filename may be chosen freely.

A default configuration file must be included in the repository.

---

## 3. Configuration

The configuration file uses:

    KEY=VALUE

Lines beginning with `#` are comments and must be ignored.

The following parameters are mandatory:

- WIDTH
- HEIGHT
- ENTRY
- EXIT
- OUTPUT_FILE
- PERFECT

Additional parameters may be supported.

For example:

    WIDTH=20
    HEIGHT=15
    ENTRY=0,0
    EXIT=19,14
    OUTPUT_FILE=maze.txt
    PERFECT=True

The program must validate configuration values and handle invalid
configuration gracefully.

Invalid configurations must produce a clear error message instead of
an unexpected crash.

---

## 4. Maze Generation

The program must generate mazes randomly.

The generated maze must:

- have the configured width and height;
- contain cells with North, East, South and West walls;
- have a valid entry position;
- have a valid exit position;
- have different entry and exit positions;
- keep entry and exit inside the maze;
- be fully connected;
- have coherent shared walls between neighbouring cells;
- have walls on the external borders;
- avoid corridors wider than two cells;
- avoid 3x3 open areas.

The maze must contain a visible `42` pattern made from several
completely closed cells.

If the maze is too small to contain the required `42` pattern, the
program must print an error message.

The generated maze must be reproducible when a seed is provided.

The maze-generation algorithm is not prescribed by these requirements.

---

## 5. Perfect Maze Mode

When:

    PERFECT=True

the generated maze must be a perfect maze.

There must be exactly one path between the entry and the exit.

The maze must not contain loops.

---

## 6. Playable Maze Mode

When:

    PERFECT=False

the generated maze must be a playable maze.

It must:

- be fully connected;
- provide open corridors at the four corners;
- provide an open corridor at the centre;
- contain at least two independent routes;
- contain loops;
- not simply be a perfect maze;
- not be created by removing only one wall from a perfect maze.

Dead ends should be rare.

Having no dead ends is a bonus.

---

## 7. Maze Cell Representation

Each cell must be represented using four wall states:

- North
- East
- South
- West

The output representation uses one hexadecimal digit per cell.

The bits are assigned as:

- bit 0: North
- bit 1: East
- bit 2: South
- bit 3: West

A closed wall is represented by `1`.

An open wall is represented by `0`.

---

## 8. Output File Format

The generated maze must be written to the configured output file.

The maze must be written row by row.

Each cell must be represented by exactly one hexadecimal digit.

After the maze grid there must be:

1. a blank line;
2. the entry coordinates;
3. the exit coordinates;
4. the shortest valid path.

The shortest path must use only:

    N
    E
    S
    W

Every output line must end with `\n`.

---

## 9. Shortest Path

The program must calculate at least one valid shortest path from the
entry to the exit.

The path must follow only open passages in the generated maze.

The path written to the output file must therefore be valid for the
generated maze.

---

## 10. Visualization

The project must provide a visual representation of the maze.

The visualization may use:

- ASCII terminal output; or
- MiniLibX.

The visualization must clearly show:

- maze walls;
- entry;
- exit;
- shortest solution path.

The interactive program must provide at least:

- regeneration/display of a new maze;
- showing/hiding the shortest path;
- changing wall colours.

Additional visual features are optional.

---

## 11. Reusable Maze Generator

The maze-generation logic must be reusable independently from the
main application.

It must be provided as a standalone module.

The reusable part must contain one unique maze-generator class, for
example:

    MazeGenerator

The generator must:

- be importable by another Python program;
- allow custom parameters such as maze size and seed;
- provide access to the generated maze structure;
- provide access to at least one solution.

The reusable module must include documentation explaining:

- how to instantiate it;
- how to use it;
- how to provide custom parameters;
- how to access the generated maze;
- how to access a solution.

The reusable module must be packaged under a name beginning with:

    mazegen-

The package must be located at the repository root.

The package must be possible to rebuild and reuse in another project.

A LICENSE.md file must be present at the repository root.

The license must explicitly allow reuse and distribution of the
generator in future projects.

---

## 12. Error Handling

The program must handle errors gracefully.

This includes, but is not limited to:

- missing configuration files;
- invalid configuration syntax;
- invalid configuration values;
- impossible maze parameters;
- invalid entry/exit positions;
- maze-generation failures;
- output-file errors.

The program must provide clear error messages.

Unexpected crashes must be avoided where errors can be handled
gracefully.

---

## 13. Code Quality

The project must use:

- Python 3.10 or newer;
- type hints;
- mypy;
- flake8;
- PEP257-compatible docstrings;
- appropriate exception handling;
- context managers where appropriate.

The project should follow clean and maintainable Python practices.

Tests are recommended.

---

## 14. Makefile

A Makefile is mandatory.

It must provide commands for:

- installing dependencies;
- running the project;
- debugging;
- cleaning generated files;
- running flake8;
- running mypy.

Strict linting may also be provided.

---

## 15. Repository Structure and Documentation

The repository must contain the required project files, including:

- `a_maze_ing.py`;
- a default configuration file;
- `Makefile`;
- `README.md`;
- `LICENSE.md`;
- `.gitignore`;
- reusable `mazegen-*` package.

The README must contain:

### Description

An explanation of the project.

### Instructions

How to install, configure and run the project.

### Resources

Resources used during development, including:

- classic references;
- AI usage.

### Configuration

The complete configuration structure and its parameters.

### Algorithm

The chosen maze-generation algorithm.

The README must explain:

- which algorithm was chosen;
- why it was chosen.

### Reusable Part

An explanation of the reusable maze-generation module and how to use
it.

### Project Management

The README must describe:

- team roles;
- project planning;
- project evolution;
- what worked;
- what could be improved;
- tools used.

Advanced features and bonuses should also be documented if implemented.

---

## 16. Bonus Features

The following are optional bonuses:

- zero dead ends by default;
- multiple maze-generation algorithms;
- maze-generation animation.

Bonus features must not compromise the mandatory requirements.

---

## 17. External Maze Analyzer

The provided `maze_analyzer.py` may be used to validate generated
mazes.

It should be treated as an external validation tool rather than as
the core implementation of the project.

The generated maze should be checked for:

- wall coherence;
- connectivity;
- loops;
- dead ends;
- perfect/playable requirements.

---

## 18. AI-Assisted Development

AI assistance may be used during development.

AI-generated code must be critically assessed.

The team remains responsible for:

- understanding the generated code;
- testing it;
- validating its behaviour;
- modifying it where necessary;
- being able to explain the implementation.

AI usage must be documented in the README.