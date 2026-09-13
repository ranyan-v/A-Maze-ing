                MazeGenerator
                     │
                     │ generate()
                     ▼
              ┌─────────────┐
              │ Create Maze │
              └──────┬──────┘
                     │
                     ▼
            reserved_cells()
                     │
                     ▼
             Check entry/exit
                     │
                     ▼
       _generate_spanning_tree()
                【DFS】
                     │
              ┌──────┴──────┐
              │             │
          perfect        Pac-Man
              │             │
              │       _add_loops()
              │             ↓
              │    _braid_dead_ends()
              │             ↓
              │   _prevent_open_areas()
              │             │
              └──────┬──────┘
                     ↓
                 return Maze

