import random
from enum import IntFlag

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

# Standard 5x7 dot-matrix bitmap for "42" (1 = wall cell, 0 = open corridor)
PATTERN_42 = [
    [1, 0, 1, 0, 1, 1, 1],
    [1, 0, 1, 0, 0, 0, 1],
    [1, 1, 1, 0, 1, 1, 1],
    [0, 0, 1, 0, 1, 0, 0],
    [0, 0, 1, 0, 1, 1, 1],
]

def apply_42_pattern(grid, visited, rows, cols):
    """Embeds the '42' pattern in the center and locks the cells."""
    p_rows = len(PATTERN_42)
    p_cols = len(PATTERN_42[0])
    
    start_r = (rows - p_rows) // 2
    start_c = (cols - p_cols) // 2

    for r in range(p_rows):
        for c in range(p_cols):
            if PATTERN_42[r][c] == 1:
                gr, gc = start_r + r, start_c + c
                grid[gr][gc] = 15       # Fully closed (ALL_WALLS)
                visited[gr][gc] = True  # Locked: DFS generator will never enter

def generate_perfect_maze(rows=21, cols=21, seed=42):
    random.seed(seed)
    grid = [[15 for _ in range(cols)] for _ in range(rows)]
    visited = [[False for _ in range(cols)] for _ in range(rows)]

    # 1. Apply and lock the 42 pattern
    apply_42_pattern(grid, visited, rows, cols)

    # 2. Pick entry and exit (corners avoid the center '42')
    entry = (0, 0)
    exit_cell = (rows - 1, cols - 1)

    # 3. Run DFS
    stack = [entry]
    visited[entry[0]][entry[1]] = True

    while stack:
        cr, cc = stack[-1]
        neighbors = []
        for direction, (dr, dc) in STEP.items():
            nr, nc = cr + dr, cc + dc
            # Notice: cells locked by 42 pattern are already visited=True, so ignored
            if 0 <= nr < rows and 0 <= nc < cols and not visited[nr][nc]:
                neighbors.append((direction, nr, nc))

        if neighbors:
            direction, nr, nc = random.choice(neighbors)
            grid[cr][cc] -= direction
            grid[nr][nc] -= OPPOSITE[direction]
            visited[nr][nc] = True
            stack.append((nr, nc))
        else:
            stack.pop()

    return grid, entry, exit_cell

def save_maze(filename, grid, entry, exit_cell):
    with open(filename, "w", encoding="utf-8") as f:
        for row in grid:
            f.write("".join(f"{cell:x}" for cell in row) + "\n")
        f.write("\n")
        # Format required by analyzer: col,row (x,y)
        f.write(f"{entry[1]},{entry[0]}\n")
        f.write(f"{exit_cell[1]},{exit_cell[0]}\n")
        f.write("DUMMY_PATH\n")

if __name__ == "__main__":
    R, C = 21, 21  # 21x21 gives plenty of room for a 5x7 pattern in the center
    grid, entry, exit_cell = generate_perfect_maze(rows=R, cols=C, seed=42)
    save_maze("step2_output.txt", grid, entry, exit_cell)
    print("Generated step2_output.txt with '42' pattern!")