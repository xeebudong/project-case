"""MarketplaceAdapter：真实平台适配器骨架。

演示如何在 BaseScraper 之上实现一个平台：翻页 URL + HTML/JSON 解析。
接入真实平台时，补全 PAGE_URL 与 parse() 的选择器/字段即可。
"""
from __future__ import annotations

from typing import Iterable

from lxml import html as lxml_html

from ..base import BaseScraper

PAGE_URL = "https://example.com/shop/list?page={page}"


class MarketplaceAdapter:
    name = "marketplace"

    def __init__(self, scraper: BaseScraper | None = None):
        self.scraper = scraper or BaseScraper(base_url="https://example.com/")

    def iter_pages(self, pages: int) -> Iterable[list[dict]]:
        self.scraper.warmup(PAGE_URL.format(page=1))
        for p in range(1, pages + 1):
            resp = self.scraper.get(PAGE_URL.format(page=p))
            items = self.parse(resp.text)
            if not items:
                break
            yield items

    @staticmethod
    def parse(text: str) -> list[dict]:
        doc = lxml_html.fromstring(text)
        out = []
        for card in doc.cssselect("div.product-card"):
            out.append({
                "sku": (card.get("data-sku") or "").strip(),
                "title": _txt(card, ".title"),
                "price": _txt(card, ".price"),
                "shop": _txt(card, ".shop-name"),
            })
        return out

    def primary_key(self, item: dict) -> str:
        return item.get("sku") or item.get("title", "")


def _txt(node, sel: str) -> str:
    found = node.cssselect(sel)
    return found[0].text_content().strip() if found else ""
