"""采集流水线：翻页 + 去重 + 增量。"""
from __future__ import annotations

import json
import logging
import os
from typing import Iterable, Protocol

log = logging.getLogger("ecom_scraper.pipeline")


class Adapter(Protocol):
    name: str

    def iter_pages(self, pages: int) -> Iterable[list[dict]]:
        ...

    def primary_key(self, item: dict) -> str:
        ...


def _load_seen(state_path: str) -> set[str]:
    if state_path and os.path.exists(state_path):
        with open(state_path, encoding="utf-8") as f:
            return set(json.load(f))
    return set()


def _save_seen(state_path: str, seen: set[str]) -> None:
    if not state_path:
        return
    os.makedirs(os.path.dirname(state_path) or ".", exist_ok=True)
    with open(state_path, "w", encoding="utf-8") as f:
        json.dump(sorted(seen), f, ensure_ascii=False)


def run(adapter: Adapter, pages: int = 5, state_path: str = "") -> list[dict]:
    """跑一遍采集，返回本次新增（增量）的条目。"""
    seen = _load_seen(state_path)
    fresh: list[dict] = []
    for pageno, batch in enumerate(adapter.iter_pages(pages), 1):
        added = 0
        for item in batch:
            key = adapter.primary_key(item)
            if key in seen:
                continue
            seen.add(key)
            fresh.append(item)
            added += 1
        log.info("page %s: +%d new (total %d)", pageno, added, len(fresh))
    _save_seen(state_path, seen)
    return fresh
