PYTHON ?= python3
PIP ?= $(PYTHON) -m pip
ENTRY ?= a_maze_ing.py
CONFIG ?= config.txt

.PHONY: all install run debug clean lint lint-strict

all: run

install:
	$(PIP) install --upgrade pip
	$(PIP) install flake8 mypy

build:
	$(PYTHON) -m build --wheel --outdir .

run:
	$(PYTHON) $(ENTRY) $(CONFIG)

debug:
	$(PYTHON) -m pdb $(ENTRY) $(CONFIG)

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete

lint:
	flake8 .
	mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	flake8 .
	mypy . --strict