# project-case

个人项目库。每个子目录是一个独立、可运行的项目，涵盖数据采集、量化研究、全栈应用、
中间件与前端。所有项目均可离线跑通，关键项目带单元测试与完整提交历史。

## 🖥 在线可视化

**打开 [`index.html`](./index.html) 或访问 GitHub Pages，点击任意项目卡片即可直接看到运行效果**
（图表 / 看板 / 页面，全部静态渲染，无需安装依赖）。

## 项目一览

| 项目 | 简介 | 技术栈 | 可视化 Demo | 一键运行 |
|------|------|--------|:----:|------|
| [ecom-scraper](./ecom-scraper) | 多平台数据采集框架：会话/限流/重试、适配器架构、增量去重、Excel 导出 | Python · requests · lxml · openpyxl | [效果](./ecom-scraper/demo.html) | `python -m ecom_scraper.cli --adapter demo` |
| [findata-quant](./findata-quant) | 量化统一数据层 + 多因子选股：Parquet 落盘、DuckDB 查询、横截面因子 | Python · Parquet · DuckDB · pandas | [效果](./findata-quant/demo.html) | `python examples/run_screen.py` |
| [ozonpulse](./ozonpulse) | 电商运营看板（全栈）：REST API + React 前端，GMV/客单价/动销/畅销榜 | FastAPI · React(Vite) · httpx | [效果](./ozonpulse/demo.html) | `uvicorn app.main:app` |
| [danmu-harvester](./danmu-harvester) | 弹幕抓取 → 结构化 → 语义分类 pipeline，可解释规则分类器 | Python · 爬虫 · 规则分类 | [效果](./danmu-harvester/demo.html) | `python harvester.py --sample` |
| [ecom-api-adapter](./ecom-api-adapter) | 多平台电商订单归一化中间件：字段映射、状态机、零依赖 | Python（标准库） | — | `python test_adapter.py` |
| [nordic-brand-site](./nordic-brand-site) | 北欧极简轻奢品牌官网，纯静态、完全响应式、CSS 设计系统 | HTML · CSS | [页面](./nordic-brand-site/index.html) | `python -m http.server 5500` |

## 亮点速览

- **ecom-scraper** — `BaseScraper` 统一会话保持、令牌桶限流、失败指数退避、UA 轮换、Cookie 门预热；适配器架构，新增平台只实现 `iter_pages`/`parse`；增量去重 + 多 Sheet Excel 导出；带单测。
- **findata-quant** — Parquet 作为单一数据真源，DuckDB 查询（缺失自动回退 pandas）；横截面因子（动量 / 波动率 / 均线多头）向量化实现；多因子打分 → 排名 → 选股，端到端离线跑通（合成 300 只票日线）。
- **ozonpulse** — 后端 FastAPI，电商平台 API 客户端（真实接口 + 无凭证自动 mock）；KPI 计算（GMV / 客单价 / 动销率 / 畅销 SKU）；前端 React + Vite 看板；hypercorn 启动规避本机 ctypes 兼容问题。
- **danmu-harvester** — 抓取/结构化/分类三段式；分类器为可解释关键词+正则，可无缝替换为向量检索或大模型。
- **ecom-api-adapter** — 注册表式适配器 + 统一状态机 + 金额/时间归一，零依赖易嵌入。
- **nordic-brand-site** — CSS 变量集中管理设计系统，桌面 4 列 → 平板 2 列 → 手机 1 列全响应式。

## 运行环境

- Python 3.10+（数据/后端项目）；Node 18+（ozonpulse 前端）
- 各子目录 `requirements.txt` / `package.json` 列出依赖；数据类项目内置离线样例，无需外部凭证即可跑通。

## 目录

```
project-case/
├── index.html            可视化总览（点击卡片看效果）
├── ecom-scraper/         数据采集框架
├── findata-quant/        量化数据层与选股
├── ozonpulse/            电商看板（全栈）
├── danmu-harvester/      弹幕抓取分类
├── ecom-api-adapter/     订单归一化中间件
└── nordic-brand-site/    品牌官网
```
