"""llm-agent: 最小多步工具调用 Agent。"""
from .core import Agent
from .llm import MockLLM

__all__ = ["Agent", "MockLLM"]
__version__ = "0.2.0"
