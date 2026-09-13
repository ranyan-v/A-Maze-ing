# B.2.1 Cell vs Maze

先只抓住一个核心概念：

Cell 是数据的最小单位，Maze 是管理这些单位的整体数据模型。
Cell is the smallest data unit; Maze is the complete data model that manages those units.

Cell 不知道：

整个迷宫有多大
Entry / Exit 在哪里
其他 Cell 是谁
怎么生成迷宫
怎么寻找路径

这些属于 Maze 的职责。

所以这是一个很典型的 separation of responsibilities（职责分离）：

Cell 描述“一个格子是什么”。
Maze 描述“整个迷宫是什么，并提供操作迷宫的方法”。

这也是为什么 Generator、Solver、Output 都可以共享同一个 Maze 对象，而不需要自己重新维护一套迷宫数据。

-----------------------------------------
# B.2.2 Position / Direction / DIRECTION_DELTAS

这三个东西其实是在解决同一个问题：

如何让程序明确、统一地表示“我从一个格子往哪个方向走到另一个格子”。
They provide a consistent way to represent movement from one cell to another.

例如：

Position = tuple[int, int]

表示：

(2, 3)

就是一个坐标。

然后：

Direction.EAST

表示“向东”。

最后：

DIRECTION_DELTAS[Direction.EAST]

得到：

(1, 0)

也就是：

(x, y)
   ↓
(x+1, y)

所以三者形成一个关系：

Position
   ↓
Direction
   ↓
Delta

例如：

(2, 3)
  + EAST (1, 0)
  = (3, 3)

这里一个很重要的设计思想是：

不要在代码各处自己写 (x + 1, y)、(x - 1, y) 等规则，而是集中定义方向规则。
Centralize movement rules instead of duplicating coordinate logic throughout the code.

这样 Generator、Solver 等其他模块都可以使用同一套方向定义。

-----------------------------------------
# B.2.3 cells[y][x] 为什么是这个顺序

这是 Python 二维 list 和我们 (x, y) 坐标之间的一个非常容易混淆的地方。


Coordinate (x, y) → List index [y][x]
坐标 (x, y) → 二维列表索引 [y][x]


为什么？

因为二维 list 的结构是：

cells
 ├── row 0  → y = 0
 ├── row 1  → y = 1
 └── row 2  → y = 2

所以：

cells[y]

先找到 第 y 行（row）。

然后：

cells[y][x]

再找到这一行中的 第 x 列（column）。

因此：

Coordinate (x, y) maps to cells[y][x].
坐标 (x, y) 在二维列表中对应 cells[y][x]。

例如：

width = 4
height = 3

坐标：

(2, 1)

意味着：

x = 2  → 第 3 列
y = 1  → 第 2 行

所以访问：

cells[1][2]

而不是：

cells[2][1]

-----------------------------------------
# B.2.4 neighbours() 和 in_bounds()

这里有一个重要的职责区分：

in_bounds() 只判断“坐标是否合法”；neighbours() 负责找出一个 Cell 周围有哪些合法邻居。
in_bounds() checks whether a position is valid; neighbours() finds the valid neighbouring cells around a position.


Neighbour（邻居）≠ Connected（连通）。

这里一定要把两个概念分开：

neighbours() → 空间上相邻 / spatially adjacent
is_open() → 是否存在可通行的连接 / whether there is a traversable connection


例如当前：

(1, 1)

如果它在一个 3 × 3 maze 的中心，那么 neighbours() 会得到：

(1, 0) NORTH
(2, 1) EAST
(1, 2) SOUTH
(0, 1) WEST

但注意：

neighbours() 不关心墙有没有打开。
neighbours() does not care whether the wall is open.

它只回答：

“这个 Cell 在物理上有哪些相邻的 Cell？”

而 is_open() 才回答：

“我能不能通过这面墙走过去？”

所以：

neighbours()
    ↓
有哪些邻居？

is_open()
    ↓
能不能通过？

这个区分之后在 Generator 和 Solver 里都会非常重要。


# B.2.5 is_open()：为什么用 bitwise AND
return not self.cell(position).walls & WALL_BITS[direction]

## bitmask（位掩码）
用一个整数的不同 bit，分别记录不同状态。
A bitmask uses different bits of one integer to represent different states.

eg.
一个 Cell 只用一个整数 walls，就可以同时保存四面墙的信息。
A single integer walls can store the state of all four walls of a cell.

walls = 1111

四个位置分别对应 N/E/S/W：

1111
|||| 
NSWE

四个都是 1 → 四面墙都关闭。

-----
每个方向拥有自己的“开关位置”。
Each direction has its own bit position.

| Direction | Bit value | Binary |
| --------- | --------: | -----: |
| N         |     `0x1` | `0001` |
| E         |     `0x2` | `0010` |
| S         |     `0x4` | `0100` |
| W         |     `0x8` | `1000` |

也就是代码里的：

WALL_BITS = {
    NORTH: 0x1,  # 1
    EAST: 0x2,   # 2
    SOUTH: 0x4,  # 4
    WEST: 0x8,   # 8
}
WALL_BITS是一个字典，方向对应bit的查表

所以当代码写：
WALL_BITS[Direction.EAST]

程序得到：
2

## bitwise AND（按位与）

walls = 1101
EAST   = 0010

我们通常从右边开始数 bit position：

bit position:  3 2 1 0
value:         1 1 0 1
               W S E N

所以：

N → bit 0 → 0001
E → bit 1 → 0010
S → bit 2 → 0100
W → bit 3 → 1000

因此 EAST 是 bit 1（第二个 bit，从右往左数）。

这也解释了为什么：

1101
&0010
----
0000

是在专门检查 EAST 那一个 bit。


# B.2.6 carve()：同时修改两个 Cell
self.cell(first).walls &= ~WALL_BITS[direction]
self.cell(second).walls &= ~WALL_BITS[opposite]

一个 passage（通道）实际上是两个相邻 Cell 共享的一面墙。
A passage is represented by the shared wall between two adjacent cells.

例如：

┌─────┬─────┐
│ A   │ B   │
│     │     │
└─────┴─────┘
       ↑
    shared wall

如果我们要从 A 向 EAST 走到 B：

A.EAST  → open
B.WEST  → open

所以：

carve(A, B)

实际上是在做：

A 的 EAST 墙：1 → 0
B 的 WEST 墙：1 → 0

------------------
怎么修改的？ 回到代码：
self.cell(first).walls &= ~WALL_BITS[direction]

其中 "&= ~" 的意思：

bit = WALL_BITS[direction]
mask = ~bit
walls = walls & mask

① ~ 是 bitwise NOT（按位取反）
0010
 ↓ ~
1101
~ 的作用：把我们想清除的那个 bit 变成 0，其余位置变成 1。
Bitwise NOT creates a mask with the target bit cleared and the other bits set.

② &= 是 bitwise AND assignment（按位与赋值）

a &= b
写成：
a = a & b

③合起来作用：
walls &= ~WALL_BITS[direction] = 把指定方向的 wall bit 清零，从而打开这面墙。
It clears the selected wall bit, thereby opening that wall.

