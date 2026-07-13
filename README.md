# 个人项目库 / Portfolio

面向 [猿急送](https://www.yuanjisong.com) 接单的工程能力展示库。每个子项目都是**可运行的真实代码**，直接对应平台上的真实需求，投递时可作为作品直接演示。

## 技能雷达
`Python 爬虫/自动化` · `全栈 Web(前端 + FastAPI)` · `AI Agent / RAG` · `跨境电商 API 对接` · `数据处理(DuckDB/Parquet)`

## 项目清单

| 项目 | 说明 | 对应需求 | 技术栈 |
|------|------|----------|--------|
| [danmu-harvester](./danmu-harvester) | 弹幕抓取 → 结构化 → 语义分类 pipeline | 159763 弹幕数据抓取分类 | Python / 爬虫 / 规则分类 |
| [nordic-brand-site](./nordic-brand-site) | 北欧极简轻奢品牌官网(全响应式) | 159765 企业官网 UI 定制 | HTML / CSS / 响应式 |
| [ecom-api-adapter](./ecom-api-adapter) | 多平台电商订单归一化中间件 | 159759 电商 API 二开 | Python / 适配器模式 |

## 如何本地跑通

```bash
# 1. 弹幕抓取分类
cd danmu-harvester
python harvester.py --sample --out danmu.json
python classifier.py --in danmu.json --out danmu_classified.json

# 2. 品牌官网
cd ../nordic-brand-site && python -m http.server 5500   # 打开 http://localhost:5500

# 3. 电商订单适配器
cd ../ecom-api-adapter && python test_adapter.py
```

## 匹配到的高契合需求(截至 2026-07-13)
- **159766** AI 自媒体运营 SaaS 开发（Agent 全栈）
- **159759** 电商 API 对接二开 ← `ecom-api-adapter`
- **159763** 弹幕数据抓取分类 ← `danmu-harvester`
- **159765** 企业官网 UI 定制 ← `nordic-brand-site`

> 详见仓库根目录 `../需求分析报告.md`（全 20 条需求爬取 + 逐条分析 + 接单策略）。
