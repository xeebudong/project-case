"""合成数据源：离线生成可复现的 A 股日线，用于跑通全链路（无需 token）。"""
from __future__ import annotations

import numpy as np
import pandas as pd


def fetch_daily(n_stocks: int = 300, n_days: int = 250, seed: int = 20240101) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    dates = pd.bdate_range("2024-01-02", periods=n_days).strftime("%Y%m%d")
    codes = [f"{i:06d}.SZ" for i in range(1, n_stocks + 1)]

    frames = []
    for code in codes:
        drift = rng.normal(0.0003, 0.0006)          # 个股漂移
        vol = rng.uniform(0.012, 0.035)             # 个股波动
        rets = rng.normal(drift, vol, n_days)
        close = 10 * np.exp(np.cumsum(rets))
        openp = close * (1 + rng.normal(0, 0.004, n_days))
        high = np.maximum(openp, close) * (1 + np.abs(rng.normal(0, 0.006, n_days)))
        low = np.minimum(openp, close) * (1 - np.abs(rng.normal(0, 0.006, n_days)))
        volu = rng.integers(1_000, 500_000, n_days).astype(float)
        frames.append(pd.DataFrame({
            "ts_code": code,
            "trade_date": dates,
            "open": openp.round(2),
            "high": high.round(2),
            "low": low.round(2),
            "close": close.round(2),
            "vol": volu,
        }))
    return pd.concat(frames, ignore_index=True)
