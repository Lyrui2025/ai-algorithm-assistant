# BFS 与 DFS 图搜索

## BFS 广度优先搜索
BFS 从起点出发，先访问距离起点最近的一层节点，再访问下一层节点。它通常使用队列实现。

典型场景：
- 无权图最短路径。
- 层序遍历。
- 迷宫最短步数。
- 社交网络关系扩散。

Python 模板：
```python
from collections import deque

def bfs(graph, start):
    visited = set([start])
    queue = deque([start])
    order = []
    while queue:
        node = queue.popleft()
        order.append(node)
        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
    return order
```

## DFS 深度优先搜索
DFS 从起点出发，沿着一条路径尽可能深入，走不通后再回溯。它可以用递归或栈实现。

典型场景：
- 连通性判断。
- 拓扑搜索。
- 路径枚举。
- 回溯问题。

## 为什么需要 visited
图中可能存在环。如果没有 `visited` 集合，搜索可能在环中反复访问同一节点，导致死循环或重复结果。

## 复杂度
对于邻接表表示的图：
- 时间复杂度：`O(V + E)`，其中 `V` 是节点数，`E` 是边数。
- 空间复杂度：`O(V)`。

## 常见错误
- 忘记初始化 `visited`。
- 入队后没有立即标记访问，导致重复入队。
- 对不存在的起点没有处理。
- 混淆 BFS 的队列和 DFS 的栈。
