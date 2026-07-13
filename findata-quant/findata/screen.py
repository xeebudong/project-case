"""多因子选股：加权打分 -> 横截面排名 -> 候选池。"""
from __future__ import annotations

import pandas as pd

from .factors import build_factor_table

# 因子权重：动量+、波动-、均线多头+
DEFAULT_WEIGHTS = {"z_mom": 1.0, "z_vol": -0.6, "z_trend": 0.8}


def score(daily: pd.DataFrame, weights: dict[str, float] | None = None) -> pd.DataFrame:
    w = weights or DEFAULT_WEIGHTS
    ft = build_factor_table(daily)
    ft["score"] = sum(ft[col] * wt for col, wt in w.items())
    ft = ft.sort_values("score", ascending=False)
    ft.insert(0, "rank", range(1, len(ft) + 1))
    return ft


def top(daily: pd.DataFrame, n: int = 20, weights: dict[str, float] | None = None) -> pd.DataFrame:
    return score(daily, weights).head(n)
