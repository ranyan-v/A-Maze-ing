"""Extension point for the unresolved ``42`` pattern requirement.

The exact bitmap, minimum dimensions, and connectivity semantics have not
been finalized.  This module intentionally reserves no cells until those
rules are decided.
"""

from typing import TypeAlias

from maze import Position

ReservedCells: TypeAlias = frozenset[Position]


def reserved_cells(width: int, height: int) -> ReservedCells:
    """Return cells reserved by the future ``42`` pattern implementation."""

    del width, height
    return frozenset()
