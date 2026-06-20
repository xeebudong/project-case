"""知识库轻量检索：对 docs/*.md 做词频打分召回（RAG-lite）。"""
from __future__ import annotations

import glob
import os
import re
from collections import Counter

_DOCS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "docs")


def _tokenize(text: str) -> list[str]:
    # 中英混合：英文单词 + 单个汉字
    return re.findall(r"[a-zA-Z]+|[一-龥]", text.lower())


class KnowledgeBase:
    def __init__(self, docs_dir: str = _DOCS_DIR):
        self.chunks: list[tuple[str, str]] = []  # (source, text)
        for path in sorted(glob.glob(os.path.join(docs_dir, "*.md"))):
            name = os.path.basename(path)
            text = open(path, encoding="utf-8").read()
            for para in re.split(r"\n\s*\n", text):
                para = para.strip()
                if len(para) >= 8:
                    self.chunks.append((name, para))

    def search(self, query: str, k: int = 2) -> list[dict]:
        q = Counter(_tokenize(query))
        scored = []
        for src, text in self.chunks:
            tf = Counter(_tokenize(text))
            score = sum(q[t] * tf[t] for t in q)
            if score:
                scored.append((score, src, text))
        scored.sort(reverse=True, key=lambda x: x[0])
        return [{"source": s, "text": t, "score": sc} for sc, s, t in scored[:k]]
