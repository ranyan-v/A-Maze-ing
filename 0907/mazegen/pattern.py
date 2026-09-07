"""Reserved '42' pattern cells for the maze generator."""

from typing import TypeAlias

from mazegen.maze import Position

ReservedCells: TypeAlias = frozenset[Position]

# 标准 5x7 点阵表示 "42" (1 代表封闭实心墙，0 代表通道走廊)
# 行高 5，列宽 7
PATTERN_42: list[list[int]] = [
    [1, 0, 1, 0, 1, 1, 1],  # █ █ ███
    [1, 0, 1, 0, 0, 0, 1],  # █ █   █
    [1, 1, 1, 0, 1, 1, 1],  # ███ ███
    [0, 0, 1, 0, 1, 0, 0],  #   █ █  
    [0, 0, 1, 0, 1, 1, 1],  #   █ ███
]


def reserved_cells(width: int, height: int) -> ReservedCells:
    """Return coordinates of cells reserved by the '42' pattern, centered in the maze."""

    p_height = len(PATTERN_42)
    p_width = len(PATTERN_42[0])

    # 如果迷宫尺寸过小无法容纳 5x7 点阵，则不绘制
    if width < p_width or height < p_height:
        return frozenset()

    # 计算水平与垂直居中偏移量 (offset_x, offset_y)
    offset_x = (width - p_width) // 2
    offset_y = (height - p_height) // 2

    cells: set[Position] = set()
    for row_idx, row in enumerate(PATTERN_42):
        for col_idx, val in enumerate(row):
            if val == 1:
                x = offset_x + col_idx
                y = offset_y + row_idx
                cells.add((x, y))

    return frozenset(cells)