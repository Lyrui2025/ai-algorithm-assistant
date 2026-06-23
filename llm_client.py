from __future__ import annotations

import os
from dataclasses import dataclass

try:
    from dotenv import load_dotenv
except ImportError:  # pragma: no cover
    load_dotenv = None

try:
    from openai import OpenAI
except ImportError:  # pragma: no cover
    OpenAI = None


@dataclass
class LLMConfig:
    api_key: str
    base_url: str
    model: str
    temperature: float = 0.2


class LLMClient:
    def __init__(self, config: LLMConfig):
        self.config = config
        if OpenAI is None:
            self.client = None
        else:
            self.client = OpenAI(api_key=config.api_key, base_url=config.base_url)

    @classmethod
    def from_env(cls) -> "LLMClient | None":
        if load_dotenv:
            load_dotenv()
        api_key = os.getenv("LLM_API_KEY", "").strip()
        base_url = os.getenv("LLM_BASE_URL", "https://api.deepseek.com").strip()
        model = os.getenv("LLM_MODEL", "deepseek-chat").strip()
        if not api_key or api_key == "your_api_key_here":
            return None
        return cls(LLMConfig(api_key=api_key, base_url=base_url, model=model))

    def complete(self, system_prompt: str, user_prompt: str) -> str:
        if self.client is None:
            raise RuntimeError("openai package is not installed. Please run: pip install -r requirements.txt")
        response = self.client.chat.completions.create(
            model=self.config.model,
            temperature=self.config.temperature,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        )
        return response.choices[0].message.content or ""


DEMO_RESPONSES = {
    "算法解释": """## 二分查找\n\n**算法思想**：在有序数组中，每次比较中间元素和目标值，将搜索范围缩小一半。\n\n**适用条件**：数组必须已经排序。\n\n**步骤**：\n1. 设置 left 和 right 指针。\n2. 计算 mid。\n3. 如果 a[mid] 等于目标值，返回位置。\n4. 如果 a[mid] 小于目标值，搜索右半部分。\n5. 如果 a[mid] 大于目标值，搜索左半部分。\n\n**复杂度**：时间复杂度 O(log n)，空间复杂度 O(1)。\n\n**注意事项**：初学者最容易忘记“数组有序”这个前提。""",
    "代码生成": """```python\ndef binary_search(nums, target):\n    left, right = 0, len(nums) - 1\n    while left <= right:\n        mid = (left + right) // 2\n        if nums[mid] == target:\n            return mid\n        if nums[mid] < target:\n            left = mid + 1\n        else:\n            right = mid - 1\n    return -1\n\nprint(binary_search([1, 3, 5, 7, 9], 7))  # 3\n```\n\n复杂度：时间 O(log n)，空间 O(1)。""",
    "测试用例": """| 类型 | 输入 | 预期输出 | 说明 |\n|---|---|---|---|\n| 正常 | nums=[1,3,5,7,9], target=7 | 3 | 目标存在 |\n| 边界 | nums=[1], target=1 | 0 | 单元素数组 |\n| 不存在 | nums=[1,3,5], target=2 | -1 | 目标不存在 |\n| 空数组 | nums=[], target=1 | -1 | 输入为空 |""",
    "报错分析": """`nums=[1,2,3]; print(nums[3])` 会出现 `IndexError`。\n\n原因：Python 列表下标从 0 开始，长度为 3 的列表合法下标是 0、1、2。`nums[3]` 访问了第 4 个元素，所以越界。\n\n修改：\n```python\nnums = [1, 2, 3]\nprint(nums[2])\n```""",
}
