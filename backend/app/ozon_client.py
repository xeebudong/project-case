"""Ozon Seller API 客户端：真实接口 + 离线 mock。"""
from __future__ import annotations

from datetime import date, timedelta

import httpx

from .config import settings
from .mock_data import gen_orders


class OzonClient:
    def __init__(self):
        self.base = settings.base_url
        self.headers = {
            "Client-Id": settings.ozon_client_id,
            "Api-Key": settings.ozon_api_key,
            "Content-Type": "application/json",
        }

    def fetch_orders(self, days: int = 7) -> list[dict]:
        """近 N 日订单。无凭证时返回 mock。"""
        if settings.mock:
            return [o for o in gen_orders(days=days)]

        since = (date.today() - timedelta(days=days)).isoformat() + "T00:00:00Z"
        to = date.today().isoformat() + "T23:59:59Z"
        payload = {
            "dir": "DESC",
            "filter": {"since": since, "to": to},
            "limit": 1000,
            "with": {"analytics_data": True},
        }
        with httpx.Client(timeout=30) as c:
            r = c.post(f"{self.base}/v3/posting/fbs/list", headers=self.headers, json=payload)
            r.raise_for_status()
            return self._normalize(r.json())

    @staticmethod
    def _normalize(raw: dict) -> list[dict]:
        out = []
        for p in raw.get("result", {}).get("postings", []):
            day = (p.get("in_process_at") or "")[:10]
            for prod in p.get("products", []):
                out.append({
                    "order_id": p.get("posting_number", ""),
                    "sku": str(prod.get("sku", "")),
                    "title": prod.get("name", ""),
                    "qty": int(prod.get("quantity", 0)),
                    "price": float(prod.get("price", 0) or 0),
                    "date": day,
                })
        return out
