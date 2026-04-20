"""端到端：合成日线 -> 落盘 Parquet -> 计算因子 -> 多因子选股 -> 打印 Top20。"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from findata import get_store
from findata.screen import top
from findata.sources import synthetic

if __name__ == "__main__":
    store = get_store()
    if not store.exists("daily"):
        daily = synthetic.fetch_daily(n_stocks=300, n_days=250)
        store.append("daily", daily, keys=["ts_code", "trade_date"])
        print(f"ingested {len(daily):,} rows -> data/daily.parquet")

    daily = store.read("daily")
    picks = top(daily, n=20)
    cols = ["rank", "momentum", "volatility", "ma_trend", "score"]
    print("\n=== 选股 Top20 ===")
    print(picks[cols].round(4).to_string())
