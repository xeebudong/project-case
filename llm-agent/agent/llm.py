"""LLM 接口：MockLLM(离线确定性) 与 AnthropicLLM(真实)。

Agent 每步向 LLM 请求一个决策：要么调用工具 {"action","input"}，要么给出 {"final"}。
"""
from __future__ import annotations

import os
import re


class LLM:
    def decide(self, task: str, steps: list[dict]) -> dict:
        raise NotImplementedError


class MockLLM(LLM):
    """确定性规划：从任务解析出工具调用序列，按已执行步数返回下一步。

    纯函数式——不依赖内部状态，便于测试与复现。
    """

    def _plan(self, task: str) -> list[dict]:
        plan: list[dict] = []
        if re.search(r"几点|现在|时间|今天|日期|now|date|time", task, re.I):
            plan.append({"action": "now", "input": ""})
        m = re.search(r"([\d\(][\d\.\+\-\*/%\(\)\s]*[\d\)])", task)
        if m and re.search(r"[\+\-\*/%]", m.group(1)):
            plan.append({"action": "calc", "input": m.group(1).strip()})
        m2 = re.search(r"查(?:一下|查)?([^，。,]+?)(?:政策|吗|$|，|。)", task)
        if re.search(r"查|政策|知识库|退货|运费|保修|policy", task, re.I):
            kw = m2.group(1).strip() if m2 else task
            plan.append({"action": "kb_search", "input": kw})
        return plan

    def decide(self, task: str, steps: list[dict]) -> dict:
        plan = self._plan(task)
        if len(steps) < len(plan):
            return plan[len(steps)]
        # 汇总为终答
        parts = []
        for s in steps:
            if s["action"] == "now":
                parts.append(f"当前时间是 {s['observation']}")
            elif s["action"] == "calc":
                parts.append(f"{s['input']} = {s['observation']}")
            elif s["action"] == "kb_search":
                parts.append(f"查询结果：{s['observation']}")
        return {"final": "；".join(parts) if parts else "我没有可用的信息来回答该问题。"}


class AnthropicLLM(LLM):
    """真实大模型适配器（需 ANTHROPIC_API_KEY 与 anthropic SDK）。

    这里给出接线骨架：把工具描述和历史组织成消息，让模型输出下一步决策。
    """

    def __init__(self, model: str = "claude-sonnet-5"):
        self.model = model

    def decide(self, task: str, steps: list[dict]) -> dict:
        import json

        from anthropic import Anthropic  # 延迟导入
        from .tools import describe_tools

        client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
        history = "\n".join(
            f"步骤{i+1}: 调用 {s['action']}({s['input']}) -> {s['observation']}"
            for i, s in enumerate(steps)
        )
        prompt = (
            f"你是一个会使用工具的助手。可用工具：\n{describe_tools()}\n\n"
            f"任务：{task}\n已执行：\n{history or '（无）'}\n\n"
            '只输出 JSON：调用工具用 {"action":"名字","input":"参数"}；'
            '已足够则用 {"final":"最终答复"}。'
        )
        resp = client.messages.create(
            model=self.model, max_tokens=512,
            messages=[{"role": "user", "content": prompt}],
        )
        return json.loads(resp.content[0].text)
