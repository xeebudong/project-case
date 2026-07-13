"""FastAPI 入口：REST 路由 + CORS。"""
from __future__ import annotations

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

from . import __version__
from .config import settings
from .models import Order, SkuStat, Summary
from .ozon_client import OzonClient
from .service import summarize, top_skus

app = FastAPI(title="OzonPulse API", version=__version__)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

client = OzonClient()


@app.get("/api/health")
def health() -> dict:
    return {"status": "ok", "mock": settings.mock, "version": __version__}


@app.get("/api/summary", response_model=Summary)
def summary(days: int = Query(7, ge=1, le=90)) -> Summary:
    return summarize(client.fetch_orders(days=days))


@app.get("/api/top-skus", response_model=list[SkuStat])
def top_sku_list(days: int = Query(30, ge=1, le=90), limit: int = Query(10, ge=1, le=50)):
    return top_skus(client.fetch_orders(days=days), limit=limit)


@app.get("/api/orders", response_model=list[Order])
def orders(days: int = Query(7, ge=1, le=90)) -> list[Order]:
    return [Order(**o) for o in client.fetch_orders(days=days)]
