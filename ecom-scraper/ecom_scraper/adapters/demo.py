"""DemoAdapter：离线演示用，生成可复现的假数据，展示流水线与导出。"""
from __future__ import annotations

import hashlib
import random
from typing import Iterable

_CATS = ["手机数码", "家居", "美妆", "母婴", "服饰", "食品"]


class DemoAdapter:
    name = "demo"

    def __init__(self, seed: int = 42, per_page: int = 20):
        self.rng = random.Random(seed)
        self.per_page = per_page

    def iter_pages(self, pages: int) -> Iterable[list[dict]]:
        sku = 100000
        for _ in range(pages):
            batch = []
            for _ in range(self.per_page):
                sku += 1
                batch.append({
                    "sku": str(sku),
                    "title": f"商品-{sku}",
                    "category": self.rng.choice(_CATS),
                    "price": self.rng.randint(9, 999),
                    "sales": self.rng.randint(0, 5000),
                    "shop": f"店铺{self.rng.randint(1, 30)}",
                })
            yield batch

    def primary_key(self, item: dict) -> str:
        return hashlib.md5(item["sku"].encode()).hexdigest()
