"""命令行入口：python -m ecom_scraper.cli --adapter demo --pages 5 --out out/demo.xlsx"""
from __future__ import annotations

import argparse
import logging

from .export import to_excel
from .pipeline import run


def _load(name: str):
    if name == "demo":
        from .adapters.demo import DemoAdapter
        return DemoAdapter()
    if name == "marketplace":
        from .adapters.marketplace import MarketplaceAdapter
        return MarketplaceAdapter()
    raise SystemExit(f"unknown adapter: {name}")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="ecom-scraper")
    ap.add_argument("--adapter", default="demo")
    ap.add_argument("--pages", type=int, default=5)
    ap.add_argument("--out", default="out/result.xlsx")
    ap.add_argument("--state", default="")
    args = ap.parse_args(argv)

    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")
    adapter = _load(args.adapter)
    items = run(adapter, pages=args.pages, state_path=args.state)
    cols = list(items[0].keys()) if items else ["sku", "title", "price"]
    to_excel(items, args.out, columns=cols, group_by="category" if "category" in cols else None)
    print(f"done: {len(items)} items -> {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
