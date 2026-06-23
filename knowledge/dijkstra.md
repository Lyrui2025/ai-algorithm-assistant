# Dijkstra 最短路径算法

## 核心思想
Dijkstra 算法用于求解非负权图中从一个起点到其他节点的最短路径。它采用贪心思想：每次选择当前距离起点最近且尚未确定的节点，并用该节点更新邻居距离。

## 适用条件
- 图的边权必须非负。
- 可以用于有向图或无向图。
- 常用于地图导航、网络路由和路径规划。

## 基本步骤
1. 初始化起点距离为 0，其他节点距离为无穷大。
2. 选择当前未确定节点中距离最小的节点。
3. 将该节点标记为已确定。
4. 遍历它的邻居，尝试用该节点更新邻居的最短距离，这一步称为松弛。
5. 重复直到所有可达节点都被确定，或目标节点被确定。

## 为什么不能处理负权边
Dijkstra 的贪心选择依赖一个前提：当前最短的未确定节点，其距离以后不会再变小。如果存在负权边，后续路径可能通过负权边把已经确定的节点距离变得更小，从而破坏贪心正确性。

## Python 思路
```python
import heapq

def dijkstra(graph, start):
    dist = {node: float('inf') for node in graph}
    dist[start] = 0
    heap = [(0, start)]
    while heap:
        current_dist, node = heapq.heappop(heap)
        if current_dist > dist[node]:
            continue
        for neighbor, weight in graph[node]:
            candidate = current_dist + weight
            if candidate < dist[neighbor]:
                dist[neighbor] = candidate
                heapq.heappush(heap, (candidate, neighbor))
    return dist
```

## 复杂度
- 使用普通数组选择最小节点：`O(V^2)`。
- 使用优先队列：`O((V + E) log V)`。

## 常见错误
- 在负权图中使用 Dijkstra。
- 忘记跳过堆中过期距离。
- 无向图只添加单向边。
- 没有处理起点或终点不存在的情况。
