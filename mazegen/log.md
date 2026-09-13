# 依赖关系
errors.py → maze.py → pattern.py → generator.py → solver.py → __init__.py

## errors.py 异常体系
所有异常都继承自 MazeError
这样调用方既可以精确捕获某一种错误
也可以用 except MazeError 一网打尽

## maze.py 核心数据结构

### 用 4 位掩码表示墙壁
WALL_BITS = {NORTH: 0x1, EAST: 0x2, SOUTH: 0x4, WEST: 0x8}
Cell.walls = 0xF  # 默认四面墙都在

每个格子只用一个 int（实际只用 4 bit）就能表示四个方向的墙是否存在

直接对应输出格式：

def hexadecimal_rows(self):
    return ["".join(format(cell.walls, "X") for cell in row) for row in self.cells]

一个格子的墙壁状态正好能编码成一位十六进制数字（0-F）

### carve() 双向开墙
def carve(self, first, second):
    direction = self._direction_between(first, second)
    opposite = OPPOSITE[direction]
    self.cell(first).walls &= ~WALL_BITS[direction]
    self.cell(second).walls &= ~WALL_BITS[opposite]

OPPOSITE 映射就是为了保证这个双向一致性

### neighbours() 只管坐标，不管墙
只负责返回网格上几何相邻的格子，完全不关心墙是否打通

## pattern.py 保留格
PATTERN_42: list[list[int]]  # 5x7 点阵，1=保留(墙内/障碍)，0=可用

reserved_cells() 返回一个 frozenset[Position]）

尺寸计算（offset_x/offset_y 居中）是自包含的
generator.py 只需要问它"哪些格子被保留"，不需要知道图案是怎么画出来的

## generator.py —— 生成算法
### DFS 生成树（Perfect Maze）

_generate_spanning_tree 是经典的"随机化迭代 DFS / recursive backtracker"算法：

维护一个栈和 visited 集合
每次看栈顶格子有没有未访问、非保留格的邻居
有的话随机选一个，carve 打通，压栈
没有就出栈（回溯）

这个算法保证生成的是一棵生成树：任意两点之间有且仅有一条路径，没有环，这就是"完美迷宫"(perfect maze) 的定义，也是 perfect=True 这个参数名的含义。

之后有个完整性检查：
if len(visited) != expected_cells:
    raise GenerationError("could not connect every maze cell")

万一保留格的形状恰好把网格分割成了几块互不相通的区域，这里就能兜底报错，而不是默默生成一个"有些格子永远走不到"的坏迷宫。

### Pac-Man 模式的后处理（perfect=False 时）
这部分是在生成树基础上"破坏"完美性，做出街机吃豆人风格的迷宫（有环路、没死胡同、没有大片空地）：

#### _add_loops
随机挑几面还关着的内墙（只从 EAST/SOUTH 方向收集，避免同一面墙被两侧各数一次），打通若干道，制造额外的环路。生成树本身是无环的，这一步专门加环。

#### _braid_dead_ends（"编织"）
找所有只剩一面墙开着的死胡同格子，给它们再打通一面墙，消除死胡同。
循环最多 5 轮是因为——打通一个死胡同可能会影响处理顺序里后面还没处理的格子（导致遍历时已经不再是死胡同了），多轮迭代能保证收敛，处理"打通开销分布不均"的边界情况。

#### _prevent_open_areas
前两步是随机的，有一定概率会连续打通形成一大片 3×3 的空地（12 面内墙全开）。
对吃豆人式迷宫来说这种"广场"是不美观/不合规的，于是扫描全图查找这种全开区域，发现了就在中心格和它北边格子之间重新砌一堵墙"打补丁"。这是修复随机过程副作用的防御性后处理，代码注释里"新增修补防护"说明这是针对某个已发现问题专门追加的逻辑。

这三步的顺序也有讲究：先加环、再消除死胡同、最后修补空地——因为加环和消除死胡同都可能制造出大片开阔区域，所以空地检测必须放在最后一步。

## solver.py —— BFS 最短路径
def shortest_path(maze: Maze) -> Solution:

标准 BFS：队列 + parents 字典记录每个格子是从哪个方向被发现的。选 BFS 而不是 DFS，是因为在无权图（每一步移动代价相同）里，BFS 第一次到达终点时走过的路径保证是最短的；DFS 做不到这个保证。

if current == maze.exit:
    break

一旦出队到 exit 就提前退出，不用等队列清空，是个小优化。

最后通过 parents 链反向回溯，把每一步的方向拼成字符串（比如 "SSEENNW"），再 reverse() 变成从入口到出口的正序——这正是题目要求的"路径输出格式"。

求解逻辑和生成逻辑完全独立（solver.py 只依赖 Maze 这个数据结构，不知道迷宫是怎么生成的），所以它也能用来验证 generator.py 生成的迷宫确实有解，或者用在单元测试里。

## __init__.py —— 对外暴露的 API
__all__ = [
    "Maze", "MazeGenerator", "Direction", "Position", "shortest_path", "MazeError", "GenerationError", "SolveError"
]

