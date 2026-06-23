from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class KnowledgeChunk:
    source: str
    title: str
    content: str
    score: int


KEYWORD_ALIASES = {
    "二分": ["二分", "binary", "binary search", "有序", "left", "right", "mid"],
    "查找": ["查找", "搜索", "search"],
    "排序": ["排序", "冒泡", "选择", "快速", "sort", "bubble", "quick"],
    "图": ["图", "节点", "边", "邻接表", "graph"],
    "BFS": ["bfs", "广度", "队列", "visited", "遍历"],
    "DFS": ["dfs", "深度", "递归", "栈", "回溯"],
    "Dijkstra": ["dijkstra", "最短路径", "负权", "松弛", "优先队列", "路径"],
    "KNN": ["knn", "近邻", "分类", "距离", "投票"],
    "错误": ["报错", "错误", "exception", "indexerror", "keyerror", "typeerror", "valueerror", "nameerror"],
    "测试": ["测试", "用例", "边界", "预期输出", "test"],
    "代码": ["代码", "模板", "python", "函数", "复杂度"],
}


def _normalize(text: str) -> str:
    return text.lower().strip()


def _tokenize_query(query: str) -> set[str]:
    normalized = _normalize(query)
    tokens = set(re.findall(r"[a-zA-Z_]+|[\u4e00-\u9fff]+|\d+", normalized))
    for key, aliases in KEYWORD_ALIASES.items():
        if key.lower() in normalized or any(alias.lower() in normalized for alias in aliases):
            tokens.update(alias.lower() for alias in aliases)
            tokens.add(key.lower())
    return {token for token in tokens if token}


def load_knowledge_files(knowledge_dir: str | Path | None = None) -> list[tuple[Path, str]]:
    base_dir = Path(knowledge_dir) if knowledge_dir else Path(__file__).resolve().parent / "knowledge"
    if not base_dir.exists():
        return []
    files = []
    for path in sorted(base_dir.glob("*.md")):
        try:
            content = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            content = path.read_text(encoding="utf-8-sig")
        if content.strip():
            files.append((path, content.strip()))
    return files


def split_markdown_sections(content: str) -> list[tuple[str, str]]:
    sections: list[tuple[str, str]] = []
    current_title = "全文"
    current_lines: list[str] = []

    for line in content.splitlines():
        if line.startswith("#"):
            if current_lines:
                sections.append((current_title, "\n".join(current_lines).strip()))
                current_lines = []
            current_title = line.lstrip("#").strip() or "未命名小节"
        else:
            current_lines.append(line)
    if current_lines:
        sections.append((current_title, "\n".join(current_lines).strip()))
    return [(title, body) for title, body in sections if body]


def _score_text(text: str, query_tokens: set[str]) -> int:
    normalized = _normalize(text)
    score = 0
    for token in query_tokens:
        if not token:
            continue
        occurrences = normalized.count(token)
        if occurrences:
            score += occurrences * min(len(token), 8)
    return score


def retrieve(query: str, top_k: int = 3, max_chars: int = 900, knowledge_dir: str | Path | None = None) -> list[KnowledgeChunk]:
    query_tokens = _tokenize_query(query)
    if not query_tokens:
        return []

    chunks: list[KnowledgeChunk] = []
    for path, content in load_knowledge_files(knowledge_dir):
        file_score = _score_text(path.stem.replace("_", " "), query_tokens)
        for title, section in split_markdown_sections(content):
            score = file_score + _score_text(title, query_tokens) * 2 + _score_text(section, query_tokens)
            if score <= 0:
                continue
            snippet = section if len(section) <= max_chars else section[:max_chars].rstrip() + "..."
            chunks.append(KnowledgeChunk(source=path.name, title=title, content=snippet, score=score))

    chunks.sort(key=lambda item: item.score, reverse=True)
    return chunks[:top_k]


def build_rag_context(chunks: list[KnowledgeChunk]) -> str:
    if not chunks:
        return ""
    parts = []
    for index, chunk in enumerate(chunks, start=1):
        parts.append(
            f"[资料 {index}] 来源：{chunk.source}；小节：{chunk.title}\n{chunk.content}"
        )
    return "\n\n".join(parts)


def format_sources(chunks: list[KnowledgeChunk]) -> list[str]:
    return [f"{chunk.source} - {chunk.title}" for chunk in chunks]
