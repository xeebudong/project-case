"""Agent 循环：plan → act → observe，直到 LLM 给出 final 或达最大步数。"""
from __future__ import annotations

from .llm import LLM, MockLLM
from .tools import REGISTRY


class Agent:
    def __init__(self, llm: LLM | None = None, max_steps: int = 6, verbose: bool = True):
        self.llm = llm or MockLLM()
        self.max_steps = max_steps
        self.verbose = verbose

    def _log(self, *a):
        if self.verbose:
            print(*a)

    def run(self, task: str) -> dict:
        steps: list[dict] = []
        self._log(f"[task] {task}")
        for i in range(self.max_steps):
            decision = self.llm.decide(task, steps)
            if "final" in decision:
                self._log(f"[final] {decision['final']}")
                return {"answer": decision["final"], "steps": steps}
            name, arg = decision["action"], decision.get("input", "")
            tool = REGISTRY.get(name)
            if not tool:
                obs = f"错误：未知工具 {name}"
            else:
                try:
                    obs = tool["fn"](arg)
                except Exception as e:  # 工具异常不崩溃，交回 Agent
                    obs = f"工具异常: {e}"
            self._log(f"  [{i+1}] {name}({arg!r}) -> {obs}")
            steps.append({"action": name, "input": arg, "observation": obs})
        return {"answer": "（达到最大步数）", "steps": steps}
