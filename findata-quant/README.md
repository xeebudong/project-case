# findata-quant

A 股量化研究的**统一数据层 + 选股流水线**。数据以 Parquet 落盘、DuckDB 做 SQL 查询
（未安装 DuckDB 时自动回退 pandas），研究与回测统一 `import findata` 读取，杜绝重复下载。

## 设计要点

- **单一数据真源**：所有行情/因子写入 `data/*.parquet`，按表分区，跨脚本复用
- **数据源可插拔**：`sources/` 下每个源实现 `fetch_daily`；内置 `synthetic` 源可离线跑通全链路
- **因子库**：动量、波动率、均线多头排列等横截面因子，向量化实现
- **选股流水线**：多因子打分 → 横截面排名 → 输出候选池
- **查询层**：`store.query("select ...")` —— 有 DuckDB 走 DuckDB，无则 pandas 兜底

## 安装

```bash
pip install -r requirements.txt   # duckdb 可选
```

## 快速开始（离线，无需 token）

```bash
python examples/run_screen.py
```

输出：合成 300 只票的日线 → 计算因子 → 打分选股 → 打印 Top20。

## 目录

```
findata/
  store.py         # Parquet 存取 + DuckDB/pandas 查询
  sources/         # 数据源适配器（synthetic / tushare 骨架）
  factors.py       # 横截面因子
  screen.py        # 多因子选股
examples/run_screen.py
```

## 接真实数据

把 `sources/tushare_source.py` 里的 token 填上、实现 `fetch_daily`，
其余流程（落盘/因子/选股）完全复用。
