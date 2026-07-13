"""KPI 计算：从订单明细算概览指标与畅销 SKU。"""
from __future__ import annotations

from collections import defaultdict

from .models import SkuStat, Summary


def summarize(orders: list[dict], catalog_size: int = 10) -> Summary:
    gmv = sum(o["price"] * o["qty"] for o in orders)
    units = sum(o["qty"] for o in orders)
    n_orders = len({o["order_id"] for o in orders})
    active_sku = len({o["sku"] for o in orders})
    return Summary(
        gmv=round(gmv, 2),
        orders=n_orders,
        units=units,
        avg_order_value=round(gmv / n_orders, 2) if n_orders else 0.0,
        active_sku_ratio=round(active_sku / catalog_size, 3) if catalog_size else 0.0,
    )


def top_skus(orders: list[dict], limit: int = 10) -> list[SkuStat]:
    agg: dict[str, dict] = defaultdict(lambda: {"units": 0, "gmv": 0.0, "title": ""})
    for o in orders:
        a = agg[o["sku"]]
        a["units"] += o["qty"]
        a["gmv"] += o["price"] * o["qty"]
        a["title"] = o["title"]
    rows = [
        SkuStat(sku=sku, title=a["title"], units=a["units"], gmv=round(a["gmv"], 2))
        for sku, a in agg.items()
    ]
    rows.sort(key=lambda s: s.gmv, reverse=True)
    return rows[:limit]
