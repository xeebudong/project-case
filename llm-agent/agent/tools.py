"""工具集：注册式，Agent 通过名字调用。新增工具只需 @tool 装饰。"""
from __future__ import annotations

import ast
import datetime
import operator as op

from .kb import KnowledgeBase

REGISTRY: dict[str, dict] = {}


def tool(name: str, desc: str):
    def deco(fn):
        REGISTRY[name] = {"fn": fn, "desc": desc}
        return fn
    return deco


# ---- 安全计算器：只允许算术表达式 ----
_OPS = {
    ast.Add: op.add, ast.Sub: op.sub, ast.Mult: op.mul,
    ast.Div: op.truediv, ast.Pow: op.pow, ast.USub: op.neg, ast.Mod: op.mod,
}


def _eval(node):
    if isinstance(node, ast.Constant):
        return node.value
    if isinstance(node, ast.BinOp):
        return _OPS[type(node.op)](_eval(node.left), _eval(node.right))
    if isinstance(node, ast.UnaryOp):
        return _OPS[type(node.op)](_eval(node.operand))
    raise ValueError("unsupported expression")


@tool("calc", "计算一个算术表达式，参数为表达式字符串，如 (23+19)*3")
def calc(expr: str) -> str:
    return str(_eval(ast.parse(expr, mode="eval").body))


@tool("now", "返回当前日期时间，无参数")
def now(_: str = "") -> str:
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


_KB = None


@tool("kb_search", "在公司知识库中检索，参数为查询关键词")
def kb_search(query: str) -> str:
    global _KB
    if _KB is None:
        _KB = KnowledgeBase()
    hits = _KB.search(query, k=2)
    if not hits:
        return "知识库未命中"
    return " | ".join(f"[{h['source']}] {h['text']}" for h in hits)


def describe_tools() -> str:
    return "\n".join(f"- {n}: {t['desc']}" for n, t in REGISTRY.items())
