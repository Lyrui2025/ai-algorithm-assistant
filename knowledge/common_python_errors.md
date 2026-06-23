# Python 常见错误 FAQ

## IndexError: list index out of range
原因：访问了列表不存在的位置。Python 列表下标从 0 开始，长度为 3 的列表合法下标是 0、1、2。

示例：
```python
nums = [1, 2, 3]
print(nums[3])  # 错误
```

修改：
```python
print(nums[2])
```

## KeyError
原因：访问字典中不存在的键。

示例：
```python
scores = {'Tom': 90}
print(scores['Jerry'])
```

修改：
```python
print(scores.get('Jerry', '不存在'))
```

## TypeError
原因：对不支持的类型执行操作，或函数参数类型不符合要求。

示例：
```python
print('score:' + 90)
```

修改：
```python
print('score:' + str(90))
```

## ValueError
原因：值的格式不符合转换要求。

示例：
```python
int('abc')
```

## NameError
原因：使用了未定义的变量或函数。

示例：
```python
print(total)
```

## 算法代码常见问题
- 二分查找边界更新不正确，导致死循环。
- BFS 忘记 `visited`，导致重复访问或死循环。
- Dijkstra 使用负权边，导致结果错误。
- 递归没有终止条件，导致 `RecursionError`。

## 调试建议
1. 先读错误类型。
2. 找到报错行号。
3. 打印关键变量。
4. 用最小输入复现问题。
5. 修改后补充测试用例。
