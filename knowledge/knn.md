# KNN K 近邻算法

## 核心思想
KNN 是一种简单的监督学习算法。对于一个待分类样本，计算它与训练集中所有样本的距离，找到距离最近的 K 个邻居，再根据这些邻居的类别投票得到预测结果。

## 适用场景
- 小规模分类任务。
- 二维数据可视化演示。
- 人工智能导论中讲解距离、分类和监督学习。

## 基本步骤
1. 准备带标签的训练样本。
2. 选择 K 值。
3. 计算新样本与所有训练样本的距离。
4. 找出距离最近的 K 个样本。
5. 对 K 个邻居的类别投票。
6. 得到预测类别。

## 常用距离
欧氏距离：
```text
distance = sqrt((x1 - x2)^2 + (y1 - y2)^2)
```

## Python 简化模板
```python
from collections import Counter
from math import sqrt

def knn_predict(points, labels, query, k=3):
    distances = []
    for point, label in zip(points, labels):
        distance = sqrt((point[0] - query[0]) ** 2 + (point[1] - query[1]) ** 2)
        distances.append((distance, label))
    nearest = sorted(distances)[:k]
    votes = Counter(label for _, label in nearest)
    return votes.most_common(1)[0][0]
```

## 复杂度
- 预测一个样本的时间复杂度：`O(n log n)`，如果只选择前 K 个可优化。
- 空间复杂度：`O(n)`。

## 常见错误
- K 值过小，模型容易受噪声影响。
- K 值过大，分类边界可能过于平滑。
- 不同特征量纲差异大时，忘记做归一化。
- 类别数量相同时没有处理平票。
