import random
from enum import IntFlag

# 1. 直接复用 analyzer 的基础定义
class Direction(IntFlag):
    NORTH = 1
    EAST = 2
    SOUTH = 4
    WEST = 8

OPPOSITE = {
    Direction.NORTH: Direction.SOUTH,
    Direction.SOUTH: Direction.NORTH,
    Direction.EAST: Direction.WEST,
    Direction.WEST: Direction.EAST,
}

STEP = {
    Direction.NORTH: (-1, 0),
    Direction.EAST: (0, 1),
    Direction.SOUTH: (1, 0),
    Direction.WEST: (0, -1),
}

# 2. 最小生成器逻辑
def generate_perfect_maze(rows=15, cols=15, seed=42):
    random.seed(seed)
    # 初始化：每格全封闭（15）
    grid = [[15 for _ in range(cols)] for _ in range(rows)]
    visited = [[False for _ in range(cols)] for _ in range(rows)]

    stack = [(0, 0)]
    visited[0][0] = True

    while stack:
        cr, cc = stack[-1]
        neighbors = []
        for direction, (dr, dc) in STEP.items():
            nr, nc = cr + dr, cc + dc
            if 0 <= nr < rows and 0 <= nc < cols and not visited[nr][nc]:
                neighbors.append((direction, nr, nc))

        if neighbors:
            direction, nr, nc = random.choice(neighbors)
            # 双向拆墙：同时扣减当前格与目标格的墙壁数值
            grid[cr][cc] -= direction
            grid[nr][nc] -= OPPOSITE[direction]
            visited[nr][nc] = True
            stack.append((nr, nc))
        else:
            stack.pop()

    return grid

# 3. 按 analyzer 的要求写入文件
def save_maze(filename, grid, entry=(0, 0), exit_cell=(14, 14)):
    with open(filename, "w", encoding="utf-8") as f:
        # 写 Hex 网格
        for row in grid:
            f.write("".join(f"{cell:x}" for cell in row) + "\n")
        # 必须写入空行隔离网格与 Footer
        f.write("\n")
        # Footer：输出格式必须是 x,y（列,行）
        f.write(f"{entry[1]},{entry[0]}\n")
        f.write(f"{exit_cell[1]},{exit_cell[0]}\n")
        f.write("DUMMY_PATH\n")

if __name__ == "__main__":
    R, C = 15, 15
    grid = generate_perfect_maze(rows=R, cols=C, seed=123)
    save_maze("my_first_maze.txt", grid, entry=(0, 0), exit_cell=(R - 1, C - 1))
    print("已成功生成 my_first_maze.txt！")