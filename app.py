from __future__ import annotations

import pandas as pd
import streamlit as st

from algorithms import (
    binary_search_trace,
    bubble_sort_steps,
    dijkstra,
    parse_int_list,
    parse_weighted_edges,
    quick_sort_steps,
    selection_sort_steps,
)
from llm_client import DEMO_RESPONSES, LLMClient
from prompts.templates import EXAMPLES, SYSTEM_PROMPT, TASK_PROMPTS
from rag import build_rag_context, format_sources, retrieve

st.set_page_config(
    page_title="AI 编程与算法应用生成助手",
    page_icon="AI",
    layout="wide",
    initial_sidebar_state="expanded",
)

CUSTOM_CSS = """
<style>
:root {
  --primary: #0f766e;
  --accent: #d97706;
  --ink: #1f2937;
  --muted: #6b7280;
  --panel: #f8fafc;
}
.block-container { padding-top: 1.5rem; padding-bottom: 2rem; }
.main-title { font-size: 2.1rem; font-weight: 760; color: var(--ink); margin-bottom: .25rem; }
.subtitle { color: var(--muted); font-size: 1rem; margin-bottom: 1.2rem; }
.metric-box { background: var(--panel); border: 1px solid #e5e7eb; border-radius: 8px; padding: .85rem; min-height: 92px; }
.metric-box b { color: var(--primary); font-size: 1.05rem; }
.small-note { color: var(--muted); font-size: .9rem; }
.step-action { border-left: 4px solid var(--primary); padding: .75rem 1rem; background: #f0fdfa; border-radius: 6px; }
.rag-box { border-left: 4px solid var(--accent); padding: .75rem 1rem; background: #fffbeb; border-radius: 6px; }
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


@st.cache_resource
def get_llm_client() -> LLMClient | None:
    return LLMClient.from_env()


def build_prompt(task: str, query: str, rag_context: str = "") -> str:
    base_prompt = TASK_PROMPTS[task].format(query=query.strip())
    if not rag_context:
        return base_prompt
    return f"""
以下是本地课程知识库检索到的资料，请优先参考这些资料回答；如果资料不足，可以结合通用算法知识补充，但不要编造不存在的资料来源。

{rag_context}

用户任务：
{base_prompt}

回答要求：
1. 明确说明回答已结合本地知识库。
2. 如果知识库资料与用户问题相关，请吸收其中的概念、模板或注意事项。
3. 保持原任务要求的输出结构。
""".strip()


def generate_answer(task: str, query: str, demo_mode: bool, rag_context: str = "") -> str:
    if demo_mode:
        prefix = "**演示模式提示：**以下为内置示例输出，未实际调用云端模型。\n\n"
        rag_note = "**RAG 提示：**已检索到本地知识库资料，真实 API 模式下会把这些资料拼入 Prompt。\n\n" if rag_context else ""
        return prefix + rag_note + DEMO_RESPONSES.get(task, DEMO_RESPONSES["算法解释"])

    client = get_llm_client()
    if client is None:
        st.warning("未检测到有效 API 配置，已切换为演示输出。请复制 .env.example 为 .env 后填写 API Key。")
        return DEMO_RESPONSES.get(task, DEMO_RESPONSES["算法解释"])
    return client.complete(SYSTEM_PROMPT, build_prompt(task, query, rag_context))


def render_sort_visualizer() -> None:
    st.subheader("排序算法可视化")
    col_a, col_b = st.columns([2, 1])
    with col_a:
        raw_values = st.text_input("输入数组", value="8, 3, 5, 1, 9, 2", help="支持逗号、空格或中文逗号分隔，最多 20 个整数。")
    with col_b:
        algorithm = st.selectbox("排序算法", ["冒泡排序", "选择排序", "快速排序"])

    try:
        values = parse_int_list(raw_values)
        if algorithm == "冒泡排序":
            steps = bubble_sort_steps(values)
        elif algorithm == "选择排序":
            steps = selection_sort_steps(values)
        else:
            steps = quick_sort_steps(values)
    except ValueError as exc:
        st.error(str(exc))
        return

    step_idx = st.slider("演示步骤", 0, len(steps) - 1, min(1, len(steps) - 1))
    step = steps[step_idx]
    chart_df = pd.DataFrame({"位置": list(range(len(step.values))), "数值": step.values})
    st.bar_chart(chart_df, x="位置", y="数值", color="#0f766e", height=320)
    st.markdown(f"<div class='step-action'><b>第 {step.index} 步：</b>{step.action}</div>", unsafe_allow_html=True)
    with st.expander("查看完整步骤表"):
        st.dataframe(pd.DataFrame([s.__dict__ for s in steps]), use_container_width=True)


def render_binary_search_demo() -> None:
    st.subheader("二分查找过程演示")
    col_a, col_b = st.columns([2, 1])
    with col_a:
        raw_values = st.text_input("有序/无序数组", value="1, 3, 5, 7, 9, 11, 13", key="binary_values")
    with col_b:
        target = st.number_input("目标值", value=7, step=1)
    try:
        values = parse_int_list(raw_values)
        trace = binary_search_trace(values, int(target))
    except ValueError as exc:
        st.error(str(exc))
        return
    st.caption("系统会先对数组排序，再展示二分查找的 left/right/mid 变化。")
    st.dataframe(pd.DataFrame(trace), use_container_width=True)


def render_dijkstra_demo() -> None:
    st.subheader("Dijkstra 最短路径查询")
    default_edges = "A B 4; A C 2; C B 1; B D 5; C D 8; C E 10; D E 2"
    raw_edges = st.text_area("输入无向带权边", value=default_edges, help="格式：A B 4; A C 2，表示 A-B 边权为 4。")
    col_a, col_b = st.columns(2)
    with col_a:
        start = st.text_input("起点", value="A")
    with col_b:
        end = st.text_input("终点", value="E")
    try:
        edges = parse_weighted_edges(raw_edges)
        path, distance, trace = dijkstra(edges, start.strip(), end.strip())
    except ValueError as exc:
        st.error(str(exc))
        return
    if distance is None:
        st.warning("起点和终点之间不存在路径。")
    else:
        st.success(f"最短路径：{' -> '.join(path)}，总距离：{distance}")
    st.dataframe(pd.DataFrame(trace), use_container_width=True)


def render_rag_sources(sources: list[str], rag_context: str) -> None:
    if not sources:
        st.info("未命中本地知识库资料，本次将使用普通 LLM 回答。")
        return
    st.markdown("<div class='rag-box'><b>已启用 RAG 知识库增强</b><br>本次回答将参考下列本地资料。</div>", unsafe_allow_html=True)
    for source in sources:
        st.caption(f"参考资料：{source}")
    with st.expander("查看检索到的知识片段"):
        st.code(rag_context, language="markdown")


def render_sidebar() -> tuple[str, bool, bool]:
    st.sidebar.title("项目控制台")
    st.sidebar.caption("面向人工智能导论与算法学习的 AI 编程助手系统")
    task = st.sidebar.radio("选择 AI 任务", list(TASK_PROMPTS.keys()))
    demo_mode = st.sidebar.toggle("演示模式", value=get_llm_client() is None, help="没有 API Key 时建议开启，保证录屏演示稳定。")
    use_rag = st.sidebar.toggle("启用课程知识库增强 RAG", value=True, help="开启后会先检索本地 knowledge 资料，再让模型基于资料回答。")
    st.sidebar.divider()
    st.sidebar.markdown("**推荐测试任务**")
    for name, example in EXAMPLES.items():
        st.sidebar.caption(f"{name}: {example}")
    st.sidebar.divider()
    st.sidebar.markdown("**模型配置**")
    if get_llm_client() is None:
        st.sidebar.warning("未读取到 .env API 配置")
    else:
        st.sidebar.success("已读取 API 配置")
    return task, demo_mode, use_rag


def main() -> None:
    task, demo_mode, use_rag = render_sidebar()
    st.markdown("<div class='main-title'>AI 编程与算法应用生成助手</div>", unsafe_allow_html=True)
    st.markdown(
        "<div class='subtitle'>围绕算法解释、代码生成、测试用例和可视化应用，帮助初学者完成从理解到运行的学习闭环。</div>",
        unsafe_allow_html=True,
    )

    col1, col2, col3, col4 = st.columns(4)
    for col, title, desc in [
        (col1, "公开 LLM", "支持 OpenAI-compatible 云端 API"),
        (col2, "Prompt + RAG", "任务模板与本地知识库增强"),
        (col3, "代码可运行", "默认 Python，包含测试和复杂度"),
        (col4, "应用演示", "排序、二分、Dijkstra 可视化"),
    ]:
        with col:
            st.markdown(f"<div class='metric-box'><b>{title}</b><br><span class='small-note'>{desc}</span></div>", unsafe_allow_html=True)

    st.divider()
    left, right = st.columns([1.08, 0.92], gap="large")

    with left:
        st.subheader("AI 生成区")
        default_query = EXAMPLES[task]
        query = st.text_area("输入你的算法/代码需求", value=default_query, height=150)
        col_run, col_clear = st.columns([1, 1])
        with col_run:
            run = st.button("生成回答", type="primary", use_container_width=True)
        with col_clear:
            show_prompt = st.button("查看 Prompt", use_container_width=True)

        chunks = retrieve(query) if use_rag else []
        rag_context = build_rag_context(chunks)
        sources = format_sources(chunks)

        if use_rag:
            render_rag_sources(sources, rag_context)

        if show_prompt:
            st.code(build_prompt(task, query, rag_context), language="markdown")

        if run:
            with st.spinner("正在生成回答..."):
                try:
                    answer = generate_answer(task, query, demo_mode, rag_context)
                except Exception as exc:  # The UI should fail visibly but gently during demos.
                    st.error(f"模型调用失败：{exc}")
                else:
                    st.markdown(answer)
                    st.session_state.setdefault("history", []).append(
                        {"task": task, "query": query, "answer": answer, "sources": sources}
                    )

        with st.expander("历史生成记录"):
            history = st.session_state.get("history", [])
            if not history:
                st.caption("暂无记录。")
            for idx, item in enumerate(reversed(history[-5:]), start=1):
                st.markdown(f"**记录 {idx}：{item['task']}**")
                st.caption(item["query"])
                if item.get("sources"):
                    st.caption("参考资料：" + "；".join(item["sources"]))
                st.markdown(item["answer"])

    with right:
        st.subheader("算法应用演示区")
        demo = st.tabs(["排序可视化", "二分查找", "最短路径"])
        with demo[0]:
            render_sort_visualizer()
        with demo[1]:
            render_binary_search_demo()
        with demo[2]:
            render_dijkstra_demo()

    st.divider()
    st.markdown(
        "**测试说明：**建议录屏时依次展示算法解释、代码生成、测试用例生成、报错分析和 RAG 参考资料，并在右侧展示排序可视化或 Dijkstra 最短路径结果。"
    )


if __name__ == "__main__":
    main()
