# AI 编程与算法应用生成助手

本项目是《人工智能导论》期末大作业配套系统，面向算法学习和 Python 编程入门场景。系统使用 Streamlit 搭建界面，通过 OpenAI-compatible 云端大模型 API 完成算法解释、代码生成、测试用例生成和报错分析，并提供排序可视化、二分查找过程演示、Dijkstra 最短路径查询等算法应用演示。

项目已加入轻量级 RAG 功能：系统会先从本地算法知识库中检索相关资料，再把检索结果拼入 Prompt，让大模型基于课程资料生成回答，并在页面展示参考资料来源。

## 1. 项目功能

- 算法解释：输入算法名称或概念，生成算法思想、适用场景、步骤、复杂度和常见误区。
- 代码生成：根据用户需求生成可运行的 Python 代码，并给出输入输出示例和复杂度分析。
- 测试用例生成：为算法代码设计正常、边界、特殊和异常测试用例。
- 报错分析：解释 Python 报错原因，给出定位方法和修改代码。
- RAG 知识库增强：检索本地 `knowledge/*.md` 资料，将相关片段作为上下文交给大模型。
- 算法可视化：支持冒泡排序、选择排序、快速排序的逐步演示。
- 应用演示：支持二分查找过程追踪和 Dijkstra 最短路径查询。
- 演示模式：未配置 API Key 或网络不稳定时，可使用内置示例输出完成界面演示。

## 2. 技术路线

- 前端与应用框架：Streamlit
- 编程语言：Python
- 大模型调用方式：OpenAI-compatible Chat Completions API
- 推荐模型：DeepSeek、Qwen、智谱、硅基流动等支持兼容接口的公开模型
- Prompt 设计：按任务拆分为算法解释、代码生成、测试用例、报错分析四类模板
- RAG 方案：本地 Markdown 知识库 + 关键词检索 + Prompt 上下文增强
- 算法应用模块：本地 Python 实现排序过程、二分查找过程、Dijkstra 最短路径过程

RAG 流程如下：

```text
用户输入问题
-> rag.py 读取 knowledge/*.md
-> 按关键词和别名检索相关知识片段
-> 将检索片段拼入 Prompt
-> 调用云端 LLM 生成回答
-> 页面展示回答和参考资料来源
```

## 3. 项目结构

```text
ai_algorithm_assistant/
|-- app.py                  # Streamlit 主应用，包含 RAG 开关和界面展示
|-- algorithms.py           # 排序、二分查找、Dijkstra 等算法演示逻辑
|-- llm_client.py           # 大模型 API 客户端与演示输出
|-- rag.py                  # 轻量级 RAG 检索模块
|-- requirements.txt        # Python 依赖
|-- .env.example            # API 配置示例
|-- prompts/
|   `-- templates.py        # Prompt 模板
|-- knowledge/              # 本地 RAG 知识库
|   |-- binary_search.md
|   |-- sorting.md
|   |-- bfs_dfs.md
|   |-- dijkstra.md
|   |-- knn.md
|   |-- common_python_errors.md
|   |-- test_design.md
|   `-- code_templates.md
|-- tests/
|   `-- test_cases.md       # 8 组测试用例与评价表
`-- docs/                   # 可放报告、截图、视频脚本
```

## 4. 环境准备

建议使用 Python 3.10 或更高版本。

进入项目目录：

```powershell
cd ai_algorithm_assistant
```

安装依赖：

```powershell
pip install -r requirements.txt
```

如果使用虚拟环境，可先执行：

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## 5. 配置大模型 API

复制配置模板：

```powershell
copy .env.example .env
```

编辑 `.env` 文件，填入自己的模型服务信息：

```env
LLM_API_KEY=你的API_KEY
LLM_BASE_URL=https://api.deepseek.com
LLM_MODEL=deepseek-chat
```

说明：

- `LLM_API_KEY`：模型平台提供的 API Key。
- `LLM_BASE_URL`：兼容 OpenAI 接口的平台地址。
- `LLM_MODEL`：调用的模型名称。
- 如果暂时没有 API Key，仍可开启页面左侧“演示模式”，使用内置示例回答完成展示。

## 6. 启动系统

在项目目录中运行：

```powershell
streamlit run app.py
```

启动后浏览器会自动打开本地页面。若没有自动打开，可在浏览器访问终端显示的本地地址，通常是：

```text
http://localhost:8501
```

## 7. 使用流程

1. 在左侧选择任务类型：算法解释、代码生成、测试用例或报错分析。
2. 根据需要开启或关闭“启用课程知识库增强 RAG”。默认建议开启。
3. 在输入框中填写算法问题、代码需求或报错信息。
4. 如已配置 API，可关闭“演示模式”；如未配置 API，可保持“演示模式”开启。
5. 页面会先显示 RAG 命中的参考资料来源，并可展开查看知识片段。
6. 点击“查看 Prompt”，可看到检索资料如何拼入 Prompt。
7. 点击“生成回答”，查看大模型输出。
8. 在右侧切换算法应用演示：排序可视化、二分查找、最短路径。

## 8. RAG 知识库说明

知识库位于：

```text
knowledge/
```

当前包含：

- `binary_search.md`：二分查找思想、代码模板、复杂度和常见错误。
- `sorting.md`：冒泡排序、选择排序、快速排序说明。
- `bfs_dfs.md`：BFS、DFS、visited 集合和图搜索说明。
- `dijkstra.md`：Dijkstra 算法、非负权限制和复杂度。
- `knn.md`：KNN 分类思想和简化代码模板。
- `common_python_errors.md`：IndexError、KeyError、TypeError 等常见错误。
- `test_design.md`：算法测试用例设计方法。
- `code_templates.md`：常用算法 Python 模板。

新增知识文件时，只需要在 `knowledge/` 下添加 `.md` 文件。建议每个文件包含：

- 标题
- 核心思想
- 适用场景
- Python 模板
- 复杂度
- 常见错误
- 测试建议

本项目采用轻量关键词检索，没有引入 FAISS、Chroma 等向量数据库。这样部署更简单、演示更稳定，也符合课程项目对 RAG 技术流程的基本要求。后续可升级为“Embedding + 向量数据库 + 语义检索”。

## 9. 推荐 RAG 演示任务

演示 RAG 时建议使用这些问题：

```text
请解释 Dijkstra 最短路径算法，说明它为什么不能处理负权边。
```

预期命中：`dijkstra.md`

```text
BFS 为什么要使用 visited 集合？
```

预期命中：`bfs_dfs.md`、`code_templates.md`

```text
为二分查找函数 binary_search(nums, target) 设计测试用例。
```

预期命中：`binary_search.md`、`test_design.md`

```text
nums=[1,2,3]\nprint(nums[3])\n为什么报错？
```

预期命中：`common_python_errors.md`

录屏时建议展示：

1. 打开“启用课程知识库增强 RAG”。
2. 输入上述问题。
3. 展示页面出现的“参考资料”。
4. 展开“查看检索到的知识片段”。
5. 点击“查看 Prompt”，证明资料已进入 Prompt。
6. 点击“生成回答”，展示模型输出。

## 10. 推荐演示视频脚本

演示视频可按以下顺序录制：

1. 项目背景：说明系统面向算法学习和 Python 初学者。
2. 模型配置：展示 `.env.example` 或侧边栏模型配置状态，说明使用公开 LLM API。
3. RAG 流程：展示 `knowledge/` 目录、RAG 开关、参考资料来源和增强 Prompt。
4. 算法解释：输入“请解释二分查找算法，并说明为什么数组必须有序”。
5. 代码生成：输入“生成一个冒泡排序 Python 函数，并统计比较次数和交换次数”。
6. 测试用例：输入“为二分查找函数 binary_search(nums, target) 设计测试用例”。
7. 报错分析：输入 `nums=[1,2,3]\nprint(nums[3])\n为什么报错？`。
8. 应用演示：展示排序可视化滑块，或展示 Dijkstra 最短路径查询结果。
9. 测试总结：展示 `tests/test_cases.md` 中的测试表，说明成功案例、失败案例和改进方向。

## 11. 测试材料

测试用例表位于：

```text
tests/test_cases.md
```

报告中可以引用其中的测试编号、输入、预期输出、实际评价和改进建议。建议至少选取 4 个成功案例和 1 个失败案例放入论文正文，其余测试放入附录或截图材料。

## 12. 常见问题

### 页面提示未读取到 API 配置

检查 `.env` 文件是否位于 `ai_algorithm_assistant` 项目目录下，并确认变量名为：

```env
LLM_API_KEY=...
LLM_BASE_URL=...
LLM_MODEL=...
```

修改 `.env` 后建议重新启动 Streamlit。

### RAG 没有命中资料

可能原因：

- 用户问题太短或关键词不明显。
- `knowledge/` 目录为空或文件不是 `.md`。
- 问题不在当前知识库范围内。

可以换成更明确的问题，例如“Dijkstra 为什么不能处理负权边”或“BFS 为什么要使用 visited”。

### 模型调用失败

可能原因包括 API Key 错误、模型名称错误、余额不足、网络不稳定或平台接口地址不兼容。可以先开启“演示模式”完成界面演示，再检查平台文档。

### Streamlit 命令不存在

说明依赖未安装成功，重新执行：

```powershell
pip install -r requirements.txt
```

### 中文显示乱码

请确认文件使用 UTF-8 编码，并使用较新的浏览器访问 Streamlit 页面。部分 Windows PowerShell 终端可能显示乱码，但不代表文件内容损坏。

## 13. 成员分工建议

- 成员 A：需求分析、系统架构、报告整合、视频脚本。
- 成员 B：模型 API 接入、Prompt 模板设计、RAG 检索流程说明。
- 成员 C：Streamlit 界面、排序可视化、二分查找和最短路径演示。
- 成员 D：知识库资料整理、测试用例设计、运行截图、失败案例分析。

## 14. AI 工具使用声明参考

本项目允许使用 AI 工具辅助完成代码编写、Prompt 优化、测试用例设计、知识库整理和报告润色，但所有模型输出均经过人工检查和运行验证。若使用外部云端 API，应在报告中说明输入数据会发送到模型服务平台，因此演示数据不包含个人隐私或敏感信息。

RAG 知识库中的资料由小组成员根据课程知识点、算法模板和常见错误整理，用于增强模型回答的依据性。系统不会直接上传真实学生隐私数据或敏感教学数据。
