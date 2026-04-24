"""tushare 数据源骨架。填入 token 并实现 fetch_daily 即可接真实行情。

注意：tushare 各接口单次返回上限不同（daily 单次约 6000 行），需按日期/代码分页拉取，
否则会被静默截断。真实实现里请查官方文档确认每个接口的 limit。
"""
from __future__ import annotations

import os

import pandas as pd

TOKEN = os.environ.get("TUSHARE_TOKEN", "")


def fetch_daily(ts_code: str = "", start: str = "", end: str = "") -> pd.DataFrame:
    if not TOKEN:
        raise RuntimeError("缺少 TUSHARE_TOKEN 环境变量")
    import tushare as ts  # 延迟导入，避免无 token 时依赖缺失报错

    pro = ts.pro_api(TOKEN)
    # 真实场景需分页；此处为最小骨架
    df = pro.daily(ts_code=ts_code, start_date=start, end_date=end)
    cols = ["ts_code", "trade_date", "open", "high", "low", "close", "vol"]
    return df[cols].sort_values("trade_date").reset_index(drop=True)
