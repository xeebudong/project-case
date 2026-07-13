# ecom-scraper

多平台电商数据采集工具包。为跨境/国内电商运营场景设计：批量抓取店铺、商品、账单数据，
自动去重、增量同步、一键导出结构化 Excel。

## 特性

- 统一的 `BaseScraper`：会话保持、失败重试、令牌桶限流、随机 UA
- 适配器架构：每个平台一个 adapter，新增平台只需实现 `fetch_page` / `parse`
- 反爬友好：Cookie 门自动预热、请求频控、指数退避
- 增量采集：按主键去重，仅抓新增
- 导出：多 Sheet Excel（明细 + 分类统计），CSV/JSON 可选

## 安装

```bash
pip install -r requirements.txt
```

## 快速开始

```bash
python -m ecom_scraper.cli --adapter demo --pages 5 --out out/demo.xlsx
```

或在代码中：

```python
from ecom_scraper.adapters.demo import DemoAdapter
from ecom_scraper.pipeline import run

items = run(DemoAdapter(), pages=5)
```

## 目录

```
ecom_scraper/
  base.py          # BaseScraper：会话/重试/限流
  pipeline.py      # 采集流水线：翻页 + 去重 + 增量
  export.py        # Excel/CSV 导出
  adapters/        # 各平台适配器
  cli.py           # 命令行入口
```

## 免责声明

仅供学习与授权范围内的数据采集使用，请遵守目标站点的 robots 与服务条款。
