import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from findata.factors import build_factor_table
from findata.screen import top
from findata.sources import synthetic
from findata.store import ParquetStore


def test_store_append_dedup():
    with tempfile.TemporaryDirectory() as d:
        store = ParquetStore(d)
        df = synthetic.fetch_daily(n_stocks=5, n_days=10)
        store.append("daily", df, keys=["ts_code", "trade_date"])
        store.append("daily", df, keys=["ts_code", "trade_date"])  # 重复写不应翻倍
        assert len(store.read("daily")) == len(df) == 50


def test_factor_table_shape():
    daily = synthetic.fetch_daily(n_stocks=30, n_days=60)
    ft = build_factor_table(daily)
    assert {"z_mom", "z_vol", "z_trend"}.issubset(ft.columns)
    assert len(ft) == 30


def test_screen_top():
    daily = synthetic.fetch_daily(n_stocks=50, n_days=120)
    picks = top(daily, n=10)
    assert len(picks) == 10
    assert list(picks["rank"]) == list(range(1, 11))
