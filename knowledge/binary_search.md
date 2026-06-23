# 二分查找 Binary Search

## 核心思想
二分查找用于在有序序列中快速定位目标值。它每次取当前搜索区间的中间位置 `mid`，比较 `nums[mid]` 与目标值 `target`，然后将搜索范围缩小到左半部分或右半部分。

## 使用前提
- 数据必须已经按升序或降序排列。
- 每次比较后，必须能够确定目标值只可能出现在某一半区间。
- 如果数组无序，二分查找的方向判断会失效。

## 基本步骤
1. 设置 `left = 0`，`right = len(nums) - 1`。
2. 当 `left <= right` 时循环。
3. 计算 `mid = (left + right) // 2`。
4. 如果 `nums[mid] == target`，返回 `mid`。
5. 如果 `nums[mid] < target`，令 `left = mid + 1`。
6. 如果 `nums[mid] > target`，令 `right = mid - 1`。
7. 循环结束仍未找到，返回 `-1`。

## Python 模板
```python
def binary_search(nums, target):
    left, right = 0, len(nums) - 1
    while left <= right:
        mid = (left + right) // 2
        if nums[mid] == target:
            return mid
        if nums[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1
```

## 复杂度
- 时间复杂度：`O(log n)`
- 空间复杂度：`O(1)`

## 常见错误
- 忘记数组必须有序。
- 循环条件写成 `left < right`，导致最后一个元素漏查。
- 更新边界时写成 `left = mid` 或 `right = mid`，可能死循环。
- 没有处理空数组。

## 测试建议
- 目标值存在于中间位置。
- 目标值存在于第一个或最后一个位置。
- 目标值不存在。
- 空数组。
- 单元素数组。
