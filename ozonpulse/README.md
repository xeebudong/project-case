# OzonPulse

面向 Ozon 跨境卖家的**运营看板**：聚合店铺订单/库存/销售数据，算好核心 KPI，前端可视化。
后端 FastAPI，前端 React（Vite）。无凭证时自动走**离线 mock**，一键跑通全链路。

## 架构

```
backend/   FastAPI + httpx
  app/ozon_client.py   Ozon Seller API 客户端（真实接口 + mock 模式）
  app/service.py       KPI 计算（GMV / 客单价 / 动销 / Top SKU）
  app/main.py          REST 路由 + CORS
frontend/  React + Vite
  src/App.jsx          看板页面
  src/api.js           调后端
```

## 运行

后端：
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload         # http://127.0.0.1:8000  文档 /docs
```
未配置 `OZON_CLIENT_ID / OZON_API_KEY` 时自动返回 mock 数据，方便前端联调。

前端：
```bash
cd frontend
npm install
npm run dev                           # http://127.0.0.1:5173
```

## 接口

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/health` | 健康检查 |
| GET | `/api/summary` | 概览 KPI（GMV/订单数/客单价/动销率） |
| GET | `/api/top-skus?limit=10` | 畅销 SKU 排行 |
| GET | `/api/orders?days=7` | 近 N 日订单明细 |

## 说明

Ozon 接口鉴权走 `Client-Id` + `Api-Key` 头；本机曾遇 ctypes 兼容问题，
生产用 hypercorn 启动更稳（见 `backend/run.py`）。
