# 个人项目库 / Portfolio

面向 [猿急送](https://www.yuanjisong.com) 接单的工程能力展示库。每个子项目都是**可运行的真实代码**，
对应平台上的真实需求，投递时可作为作品直接演示。

## 技能雷达
`Python 爬虫/自动化` · `全栈 Web(React + FastAPI)` · `AI Agent / RAG` · `跨境电商 API 对接` · `A股量化` · `数据处理(DuckDB/Parquet)`

## 旗舰项目（各自独立 git 仓库，可单独推 GitHub）

| 项目 | 方向 | 技术栈 | 一键跑通 | 提交 |
|------|------|--------|----------|------|
| [ecom-scraper](./ecom-scraper) | 爬虫 / 电商数据采集 | Python · requests · lxml · openpyxl | `python -m ecom_scraper.cli --adapter demo` | 8 |
| [findata-quant](./findata-quant) | A股量化数据层 / 选股 | Python · Parquet · DuckDB · pandas | `python examples/run_screen.py` | 7 |
| [ozonpulse](./ozonpulse) | 跨境电商运营看板(全栈) | FastAPI · React(Vite) · httpx | `uvicorn app.main:app` + `npm run dev` | 11 |

**亮点**
- **ecom-scraper**：`BaseScraper` 会话/重试/令牌桶限流/UA 轮换/Cookie 门预热；适配器架构；增量去重 + 多 Sheet Excel 导出；带单测。
- **findata-quant**：Parquet 落盘 + DuckDB 查询(缺失回退 pandas)，统一数据源；横截面因子(动量/波动/均线多头)；多因子选股端到端跑通。
- **ozonpulse**：Ozon Seller API 客户端(真实接口+mock)；KPI(GMV/客单价/动销/畅销榜)；React 看板；hypercorn 规避 ctypes 坑。

## 早期项目（本 monorepo 内）

| 项目 | 说明 | 对应需求 | 技术栈 |
|------|------|----------|--------|
| [danmu-harvester](./danmu-harvester) | 弹幕抓取 → 结构化 → 语义分类 pipeline | 159763 弹幕数据抓取分类 | Python / 爬虫 / 规则分类 |
| [nordic-brand-site](./nordic-brand-site) | 北欧极简轻奢品牌官网(全响应式) | 159765 企业官网 UI 定制 | HTML / CSS / 响应式 |
| [ecom-api-adapter](./ecom-api-adapter) | 多平台电商订单归一化中间件 | 159759 电商 API 二开 | Python / 适配器模式 |

## 如何跑通

```bash
# 旗舰：电商爬虫（离线）
cd ecom-scraper && python -m ecom_scraper.cli --adapter demo --pages 5 --out out/demo.xlsx

# 旗舰：量化选股（离线）
cd findata-quant && python examples/run_screen.py

# 旗舰：跨境看板（后端 mock 模式）
cd ozonpulse/backend && uvicorn app.main:app --reload   # 文档 /docs

# 早期：弹幕抓取分类
cd danmu-harvester && python harvester.py --sample --out danmu.json

# 早期：品牌官网
cd nordic-brand-site && python -m http.server 5500
```

## 如何展示给客户
1. 三个旗舰项目各自 `git push` 到 GitHub / Gitee（公开仓库），链接放进猿急送「案例展示」；
2. 或直接把本目录打包发给需求方；
3. 每个仓库 README 都有"一键跑通"命令，客户可自行验证。

> 需求分析与接单策略见 `../` 目录：`猿急送全站需求分类.xlsx`、`我的兴趣机会单.xlsx`、`我的简历_猿急送.md`。
