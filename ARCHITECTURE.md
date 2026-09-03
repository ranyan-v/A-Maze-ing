# B.1 第一件事：确定核心模块

根据刚才的 requirements，我建议先从这几个角色开始：
a_maze_ing.py
     │
     ▼
  Config
     │
     ▼
   Maze
     │
     ├──────────────┐
     ▼              ▼
Generator         Solver
     │              │
     └──────┬───────┘
            ▼
         Output
            │
            ▼
       Visualizer

对应职责：

Module	Responsibility
Config	读取、解析、验证 configuration
Maze	保存和管理 maze 的数据结构
Generator	生成 maze
Solver	找到 shortest path
Output	按 PDF 要求写入文件
Visualizer	显示和交互
a_maze_ing.py	协调整个程序流程

这里有一个非常重要的 Architecture 原则：

Separation of responsibilities（职责分离）：每个模块负责一个清晰的职责，而不是让一个 class/function 什么都做。

例如：
Generator
    ↓
creates Maze

Solver
    ↓
reads Maze

Output
    ↓
reads Maze + solution


# B.2：Maze 是什么

Maze 是整个程序共享的“迷宫本体”

Maze data model（迷宫数据模型） = 用一个结构保存：

maze 的 width / height
每个 cell 的墙
entry
exit

可以先把它想象成：
Maze
│
├── width
├── height
├── entry
├── exit
│
└── cells
     ├── cell
     ├── cell
     ├── cell
     └── ...

然后其他模块都围绕这个 Maze 工作：
Generator  → 创建/修改 Maze
Solver     → 读取 Maze，寻找 path
Output     → 读取 Maze，写文件
Visualizer → 读取 Maze，显示

所以 Maze 本身不是负责“生成、求解、显示”的东西。

它更像是：

The data model represents what the maze currently is.
数据模型只描述“迷宫现在是什么样子”。

这就是我们之前说的 Separation of responsibilities（职责分离） 在实际项目中的第一个具体例子。


# B.3：Generator 是什么

**Generator（迷宫生成器）**的职责非常单纯：

Generate a valid Maze（生成一个符合要求的 Maze）。

也就是说：
Generator
    ↓
   Maze

它负责决定：

哪些墙打开
哪些墙关闭
最终 maze 是否满足对应模式的要求

但它不负责：

读取 config 文件
找 shortest path
写 output file
显示画面

这些交给其他模块。

这里有一个对我们之后很重要的概念

我们可以把：

Generator

看成一个角色（responsibility），而不是现在就等于某一种算法。
以后可能是：

Generator
   ├── DFS
   ├── Prim
   └── Kruskal

所以：

Generation algorithm（生成算法）是 Generator 的实现方式，而 Generator 是它承担的职责。


# B.4：Solver 是什么
**Solver（迷宫求解器）**的职责是：

Read a Maze and find a valid shortest path from the entry to the exit.
读取现有的 Maze，并找到从入口到出口的一条有效最短路径。

所以它的关系是：

Maze
  │
  ▼
Solver
  │
  ▼
Path

注意一个非常重要的区别：

Generator 修改/创建 Maze；Solver 不负责生成 Maze。
例如：

Generator
   ↓
Maze
   ↓
Solver
   ↓
N E E S S ...

这里最后的 N E E S S... 就是 PDF 要求写进 output 的 shortest path。

我们之前已经学过 **BFS（Breadth-First Search，广度优先搜索）**可以用于这种 shortest-path 问题，所以后面我们会看到它是否适合作为实现方案。



# B.5：Output 是什么

**Output（输出模块）**的职责：

Convert the Maze and its solution into the required output-file format.
把 Maze 和它的 solution 转换成 PDF 要求的输出文件格式。

所以：

Maze + Path
     ↓
   Output
     ↓
  maze.txt

它需要处理我们刚才 Requirement 里规定的格式，例如：

A3F...
...
<blank line>
entry
exit
path

但它不应该负责生成 maze，也不应该负责寻找 shortest path。

也就是说：

Generator → Maze
Solver    → Path
Output    → File

这是三个不同的 responsibility（职责）。


# B.6：Visualizer 是什么

**Visualizer（可视化模块）**的职责：

Display the current Maze and provide the required user interactions.
显示当前 Maze，并提供 PDF 要求的交互功能。

它从 Maze 和 Path 获取信息：

Maze ───────┐
            ▼
         Visualizer
            ▲
Path ───────┘

它负责的是“让人看到和操作迷宫”，而不是生成迷宫。

根据 Requirement，它至少需要支持：

显示 maze
重新生成 / 显示新的 maze
显示 / 隐藏 shortest path
改变 wall colours

PDF 允许我们选择：

ASCII terminal
MiniLibX

所以这里暂时也不用决定具体使用哪一个。

# 小总结

我们的核心模块就变成：

Config       → configuration
Maze         → maze data
Generator    → generate maze
Solver       → find path
Output       → save file
Visualizer   → display & interact

这是 Architecture 里最主要的 6 个角色。

# B.7：把模块连起来——Data Flow（数据流）
把刚才的 6 个模块放到一次完整运行里：
Config
  ↓
读取并验证参数
  ↓
Generator
  ↓
生成 Maze
  ↓
Solver
  ↓
找到 shortest Path
  ↓
Output
  ↓
写入 output file

Maze + Path
  ↓
Visualizer
  ↓
显示和交互

这里有一个很重要的 Architecture 概念：
Maze 是中间的核心数据
              ┌→ Solver → Path → Output
              │
Config → Generator → Maze
              │
              └→ Visualizer

Generator 生成的 Maze 可以被多个模块使用。

因此我们不需要：

Generator → Solver
Generator → Output
Generator → Visualizer

每个模块直接互相调用。

而是让它们围绕 **Maze data model（迷宫数据模型）**协作。

这就是我们现在 Architecture 的核心思想。

