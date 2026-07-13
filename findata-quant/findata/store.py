"""Parquet 数据层：按表落盘，DuckDB/pandas 双查询后端。"""
from __future__ import annotations

import os
from functools import lru_cache

import pandas as pd

try:
    import duckdb  # type: ignore
    _HAS_DUCKDB = True
except ImportError:  # 本机无 duckdb 时回退 pandas
    _HAS_DUCKDB = False

DATA_DIR = os.environ.get("FINDATA_DIR", os.path.join(os.getcwd(), "data"))


class ParquetStore:
    """一张表 = 一个 parquet 文件。write 覆盖，append 增量合并去重。"""

    def __init__(self, data_dir: str = DATA_DIR):
        self.data_dir = data_dir
        os.makedirs(data_dir, exist_ok=True)

    def _path(self, table: str) -> str:
        return os.path.join(self.data_dir, f"{table}.parquet")

    def exists(self, table: str) -> bool:
        return os.path.exists(self._path(table))

    def write(self, table: str, df: pd.DataFrame) -> None:
        df.to_parquet(self._path(table), index=False)

    def append(self, table: str, df: pd.DataFrame, keys: list[str]) -> None:
        if self.exists(table):
            old = self.read(table)
            df = pd.concat([old, df], ignore_index=True)
        df = df.drop_duplicates(subset=keys, keep="last").reset_index(drop=True)
        self.write(table, df)

    def read(self, table: str) -> pd.DataFrame:
        if not self.exists(table):
            raise FileNotFoundError(f"table not found: {table}")
        return pd.read_parquet(self._path(table))

    def query(self, sql: str) -> pd.DataFrame:
        """SQL 查询。表名用文件名（不含扩展名）。有 DuckDB 用 DuckDB，否则简单回退。"""
        if _HAS_DUCKDB:
            con = duckdb.connect()
            for fn in os.listdir(self.data_dir):
                if fn.endswith(".parquet"):
                    name = fn[:-8]
                    con.execute(
                        f"create view {name} as select * from read_parquet('{self._path(name)}')"
                    )
            try:
                return con.execute(sql).df()
            finally:
                con.close()
        raise RuntimeError("DuckDB 未安装：请用 read()/pandas 接口，或 pip install duckdb")


@lru_cache(maxsize=1)
def get_store() -> ParquetStore:
    return ParquetStore()
