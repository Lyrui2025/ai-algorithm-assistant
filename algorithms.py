from __future__ import annotations

from dataclasses import dataclass
import heapq
from typing import Iterable, List, Tuple


@dataclass(frozen=True)
class SortStep:
    index: int
    values: List[int]
    action: str
    highlight: Tuple[int, int] | None = None


def parse_int_list(raw: str) -> List[int]:
    """Parse comma/space separated integers for the visual demos."""
    cleaned = raw.replace("，", ",").replace(";", ",").replace(" ", ",")
    values = []
    for part in cleaned.split(","):
        part = part.strip()
        if not part:
            continue
        values.append(int(part))
    if not values:
        raise ValueError("请输入至少一个整数。")
    if len(values) > 20:
        raise ValueError("为了保证演示清晰，最多输入 20 个整数。")
    return values


def bubble_sort_steps(values: Iterable[int]) -> List[SortStep]:
    arr = list(values)
    steps = [SortStep(0, arr.copy(), "初始数组")]
    step_no = 1
    n = len(arr)
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            steps.append(
                SortStep(step_no, arr.copy(), f"比较 a[{j}]={arr[j]} 和 a[{j + 1}]={arr[j + 1]}", (j, j + 1))
            )
            step_no += 1
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
                steps.append(SortStep(step_no, arr.copy(), f"交换位置 {j} 和 {j + 1}", (j, j + 1)))
                step_no += 1
        if not swapped:
            steps.append(SortStep(step_no, arr.copy(), "本轮没有交换，数组已有序，提前结束"))
            break
    steps.append(SortStep(step_no + 1, arr.copy(), "排序完成"))
    return steps


def selection_sort_steps(values: Iterable[int]) -> List[SortStep]:
    arr = list(values)
    steps = [SortStep(0, arr.copy(), "初始数组")]
    step_no = 1
    n = len(arr)
    for i in range(n - 1):
        min_idx = i
        steps.append(SortStep(step_no, arr.copy(), f"从位置 {i} 开始寻找最小值", (i, i)))
        step_no += 1
        for j in range(i + 1, n):
            steps.append(SortStep(step_no, arr.copy(), f"比较当前最小值 a[{min_idx}]={arr[min_idx]} 与 a[{j}]={arr[j]}", (min_idx, j)))
            step_no += 1
            if arr[j] < arr[min_idx]:
                min_idx = j
                steps.append(SortStep(step_no, arr.copy(), f"更新最小值位置为 {min_idx}", (i, min_idx)))
                step_no += 1
        if min_idx != i:
            arr[i], arr[min_idx] = arr[min_idx], arr[i]
            steps.append(SortStep(step_no, arr.copy(), f"将最小值交换到位置 {i}", (i, min_idx)))
            step_no += 1
    steps.append(SortStep(step_no, arr.copy(), "排序完成"))
    return steps


def quick_sort_steps(values: Iterable[int]) -> List[SortStep]:
    arr = list(values)
    steps = [SortStep(0, arr.copy(), "初始数组")]
    step_no = 1

    def partition(low: int, high: int) -> int:
        nonlocal step_no
        pivot = arr[high]
        steps.append(SortStep(step_no, arr.copy(), f"选择 a[{high}]={pivot} 作为基准", (high, high)))
        step_no += 1
        i = low - 1
        for j in range(low, high):
            steps.append(SortStep(step_no, arr.copy(), f"比较 a[{j}]={arr[j]} 与基准 {pivot}", (j, high)))
            step_no += 1
            if arr[j] <= pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
                steps.append(SortStep(step_no, arr.copy(), f"把较小元素放到左侧：交换 {i} 和 {j}", (i, j)))
                step_no += 1
        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        steps.append(SortStep(step_no, arr.copy(), f"基准归位到位置 {i + 1}", (i + 1, high)))
        step_no += 1
        return i + 1

    def sort(low: int, high: int) -> None:
        if low < high:
            pi = partition(low, high)
            sort(low, pi - 1)
            sort(pi + 1, high)

    sort(0, len(arr) - 1)
    steps.append(SortStep(step_no, arr.copy(), "排序完成"))
    return steps


def binary_search_trace(values: Iterable[int], target: int) -> List[dict]:
    arr = sorted(values)
    left, right = 0, len(arr) - 1
    trace = []
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            trace.append({"left": left, "right": right, "mid": mid, "mid_value": arr[mid], "decision": "找到目标"})
            return trace
        if arr[mid] < target:
            trace.append({"left": left, "right": right, "mid": mid, "mid_value": arr[mid], "decision": "中间值偏小，搜索右半部分"})
            left = mid + 1
        else:
            trace.append({"left": left, "right": right, "mid": mid, "mid_value": arr[mid], "decision": "中间值偏大，搜索左半部分"})
            right = mid - 1
    trace.append({"left": left, "right": right, "mid": None, "mid_value": None, "decision": "未找到目标"})
    return trace


def parse_weighted_edges(raw: str) -> list[tuple[str, str, int]]:
    edges = []
    for line in raw.replace("；", ";").split(";"):
        line = line.strip()
        if not line:
            continue
        parts = [p.strip() for p in line.replace(",", " ").split()]
        if len(parts) != 3:
            raise ValueError("边格式应为：A B 4; A C 2")
        source, target, weight_raw = parts
        weight = int(weight_raw)
        if weight < 0:
            raise ValueError("Dijkstra 算法要求边权非负。")
        edges.append((source, target, weight))
    if not edges:
        raise ValueError("请输入至少一条边。")
    return edges


def dijkstra(edges: Iterable[tuple[str, str, int]], start: str, end: str) -> tuple[list[str], int | None, list[dict]]:
    graph: dict[str, list[tuple[str, int]]] = {}
    for source, target, weight in edges:
        graph.setdefault(source, []).append((target, weight))
        graph.setdefault(target, []).append((source, weight))
    if start not in graph or end not in graph:
        raise ValueError("起点或终点不在图中。")

    dist = {node: float("inf") for node in graph}
    prev: dict[str, str | None] = {node: None for node in graph}
    dist[start] = 0
    queue = [(0, start)]
    visited = set()
    trace = []

    while queue:
        current_dist, node = heapq.heappop(queue)
        if node in visited:
            continue
        visited.add(node)
        trace.append({"node": node, "distance": current_dist, "action": f"确定 {node} 的最短距离为 {current_dist}"})
        if node == end:
            break
        for neighbor, weight in graph[node]:
            candidate = current_dist + weight
            if candidate < dist[neighbor]:
                dist[neighbor] = candidate
                prev[neighbor] = node
                heapq.heappush(queue, (candidate, neighbor))
                trace.append({"node": neighbor, "distance": candidate, "action": f"更新 {neighbor}：经由 {node}，距离 {candidate}"})

    if dist[end] == float("inf"):
        return [], None, trace

    path = []
    current: str | None = end
    while current is not None:
        path.append(current)
        current = prev[current]
    path.reverse()
    return path, int(dist[end]), trace
