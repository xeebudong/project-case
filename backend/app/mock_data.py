"""离线 mock 订单：可复现，供无凭证时联调。"""
from __future__ import annotations

import random
from datetime import date, timedelta

_TITLES = [
    ("SKU-1001", "无线蓝牙耳机"), ("SKU-1002", "便携充电宝 20000mAh"),
    ("SKU-1003", "机械键盘 87 键"), ("SKU-1004", "USB-C 快充线 2m"),
    ("SKU-1005", "手机支架 铝合金"), ("SKU-1006", "智能手表 运动版"),
    ("SKU-1007", "降噪耳塞"), ("SKU-1008", "车载充电器"),
    ("SKU-1009", "无线鼠标 静音"), ("SKU-1010", "笔记本支架"),
]


def gen_orders(days: int = 30, seed: int = 7) -> list[dict]:
    rng = random.Random(seed)
    today = date(2026, 6, 30)
    out = []
    oid = 50000
    for d in range(days):
        day = (today - timedelta(days=d)).isoformat()
        for _ in range(rng.randint(8, 25)):
            oid += 1
            sku, title = rng.choice(_TITLES)
            out.append({
                "order_id": f"OZ{oid}",
                "sku": sku,
                "title": title,
                "qty": rng.randint(1, 3),
                "price": round(rng.uniform(9.9, 89.9), 2),
                "date": day,
            })
    return out
