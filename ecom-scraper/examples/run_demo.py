"""离线跑通：无需联网，演示采集 -> 增量去重 -> Excel。"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ecom_scraper.adapters.demo import DemoAdapter
from ecom_scraper.export import to_excel
from ecom_scraper.pipeline import run

if __name__ == "__main__":
    items = run(DemoAdapter(), pages=5)
    to_excel(items, "out/demo.xlsx",
             columns=["sku", "title", "category", "price", "sales", "shop"],
             group_by="category")
    print(f"{len(items)} items -> out/demo.xlsx")
