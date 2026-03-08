"""Pydantic 数据模型。"""
from __future__ import annotations

from pydantic import BaseModel


class Order(BaseModel):
    order_id: str
    sku: str
    title: str
    qty: int
    price: float
    date: str  # YYYY-MM-DD


class Summary(BaseModel):
    gmv: float
    orders: int
    units: int
    avg_order_value: float
    active_sku_ratio: float


class SkuStat(BaseModel):
    sku: str
    title: str
    units: int
    gmv: float
