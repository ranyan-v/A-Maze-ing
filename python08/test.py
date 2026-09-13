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
print("Solution steps:\n",path)

# Export hex rows
for row in maze.hexadecimal_rows():
    print(row)