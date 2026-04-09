"""findata-quant: A 股量化统一数据层。"""
from .store import ParquetStore, get_store

__version__ = "0.6.1"
__all__ = ["ParquetStore", "get_store"]
