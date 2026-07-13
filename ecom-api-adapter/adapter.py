# -*- coding: utf-8 -*-
"""
ecom-api-adapter —— 多平台电商订单 API 归一化中间件

不同电商平台(Ozon / Shopify / 拼多多...)订单字段各不相同，本模块把它们
统一映射为内部标准订单模型 UnifiedOrder，屏蔽上游差异，便于二次开发。
纯标准库实现，零依赖，可直接单测。
"""
from __future__ import annotations
from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import List, Dict, Callable


@dataclass
class UnifiedItem:
    sku: str
    title: str
    qty: int
    price: float          # 单价(元)


@dataclass
class UnifiedOrder:
    platform: str
    order_no: str
    status: str           # created / paid / shipped / done / cancelled
    currency: str
    total: float
    buyer: str
    created_at: str       # ISO8601
    items: List[UnifiedItem] = field(default_factory=list)


# 各平台状态 -> 统一状态
STATUS_MAP: Dict[str, Dict[str, str]] = {
    "ozon":    {"awaiting_packaging": "paid", "delivering": "shipped",
                "delivered": "done", "cancelled": "cancelled"},
    "shopify": {"pending": "created", "paid": "paid",
                "fulfilled": "shipped", "cancelled": "cancelled"},
    "pdd":     {"1": "created", "2": "paid", "3": "shipped", "5": "done", "0": "cancelled"},
}


def _iso(ts) -> str:
    if isinstance(ts, (int, float)):
        return datetime.utcfromtimestamp(ts).isoformat() + "Z"
    return str(ts)


def from_ozon(raw: dict) -> UnifiedOrder:
    items = [UnifiedItem(p["sku"], p["name"], p["quantity"], float(p["price"]))
             for p in raw.get("products", [])]
    return UnifiedOrder(
        platform="ozon", order_no=raw["posting_number"],
        status=STATUS_MAP["ozon"].get(raw["status"], raw["status"]),
        currency=raw.get("currency_code", "CNY"),
        total=sum(i.price * i.qty for i in items),
        buyer=raw.get("customer", {}).get("name", ""),
        created_at=_iso(raw.get("in_process_at")), items=items)


def from_shopify(raw: dict) -> UnifiedOrder:
    items = [UnifiedItem(str(li["sku"]), li["title"], li["quantity"], float(li["price"]))
             for li in raw.get("line_items", [])]
    return UnifiedOrder(
        platform="shopify", order_no=str(raw["name"]),
        status=STATUS_MAP["shopify"].get(raw["financial_status"], raw["financial_status"]),
        currency=raw.get("currency", "USD"),
        total=float(raw.get("total_price", sum(i.price * i.qty for i in items))),
        buyer=raw.get("customer", {}).get("first_name", ""),
        created_at=_iso(raw.get("created_at")), items=items)


def from_pdd(raw: dict) -> UnifiedOrder:
    items = [UnifiedItem(g["goods_id"], g["goods_name"], g["goods_count"],
                         float(g["goods_price"]) / 100.0)
             for g in raw.get("item_list", [])]
    return UnifiedOrder(
        platform="pdd", order_no=raw["order_sn"],
        status=STATUS_MAP["pdd"].get(str(raw["order_status"]), str(raw["order_status"])),
        currency="CNY",
        total=float(raw.get("order_amount", 0)) / 100.0,
        buyer=raw.get("receiver_name", ""),
        created_at=_iso(raw.get("created_time")), items=items)


ADAPTERS: Dict[str, Callable[[dict], UnifiedOrder]] = {
    "ozon": from_ozon, "shopify": from_shopify, "pdd": from_pdd,
}


def normalize(platform: str, raw: dict) -> UnifiedOrder:
    if platform not in ADAPTERS:
        raise ValueError(f"unsupported platform: {platform}")
    return ADAPTERS[platform](raw)


def normalize_batch(payload: Dict[str, List[dict]]) -> List[dict]:
    out = []
    for platform, orders in payload.items():
        for raw in orders:
            out.append(asdict(normalize(platform, raw)))
    return out
