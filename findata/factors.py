"""横截面因子库：输入长表日线，输出每只票在最新截面的因子值。"""
from __future__ import annotations

import numpy as np
import pandas as pd


def _close_panel(daily: pd.DataFrame) -> pd.DataFrame:
    """长表 -> 宽表 close 面板：index=trade_date, columns=ts_code。"""
    panel = daily.pivot(index="trade_date", columns="ts_code", values="close")
    return panel.sort_index()


def momentum(daily: pd.DataFrame, window: int = 20) -> pd.Series:
    """N 日动量（收益率）。"""
    px = _close_panel(daily)
    return (px.iloc[-1] / px.iloc[-1 - window] - 1).rename("momentum")


def volatility(daily: pd.DataFrame, window: int = 20) -> pd.Series:
    """N 日收益波动率（越低越好，打分时取负）。"""
    px = _close_panel(daily)
    rets = px.pct_change().iloc[-window:]
    return rets.std().rename("volatility")


def ma_trend(daily: pd.DataFrame, short: int = 5, long: int = 20) -> pd.Series:
    """均线多头强度：MA_short / MA_long - 1。"""
    px = _close_panel(daily)
    ma_s = px.iloc[-short:].mean()
    ma_l = px.iloc[-long:].mean()
    return (ma_s / ma_l - 1).rename("ma_trend")


def zscore(s: pd.Series) -> pd.Series:
    """横截面标准化。"""
    mu, sd = s.mean(), s.std(ddof=0)
    return (s - mu) / sd if sd else s * 0.0


def build_factor_table(daily: pd.DataFrame) -> pd.DataFrame:
    mom = momentum(daily)
    vol = volatility(daily)
    trend = ma_trend(daily)
    df = pd.concat([mom, vol, trend], axis=1).dropna()
    df["z_mom"] = zscore(df["momentum"])
    df["z_vol"] = zscore(df["volatility"])
    df["z_trend"] = zscore(df["ma_trend"])
    return df
