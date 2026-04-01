"""生产启动：用 hypercorn 规避本机 uvicorn+ctypes 兼容问题。"""
import asyncio

from hypercorn.asyncio import serve
from hypercorn.config import Config

from app.main import app

if __name__ == "__main__":
    cfg = Config()
    cfg.bind = ["0.0.0.0:8000"]
    asyncio.run(serve(app, cfg))
