# llm-agent

一个**最小但完整**的多步工具调用 Agent：接收自然语言任务 → 规划 → 调用工具 → 观察结果 → 循环 → 汇总答案。
内置**确定性 MockLLM**，无需任何 API Key 即可离线跑通整套 agent 循环；接真实大模型只需实现一个 `LLM` 适配器。

## 特性

- **Agent 循环**：`plan → act → observe` 迭代，带最大步数与终止判断
- **工具系统**：注册式工具（计算器、日期、知识库检索），`@tool` 装饰器即插即用
- **RAG-lite**：`docs/` 下的知识库用轻量 TF 检索召回，作为一个工具供 Agent 调用
- **可插拔 LLM**：`MockLLM`（离线、确定性）/ `AnthropicLLM`（填 key 即用）同一接口
- **可观测**：每一步的思考、工具调用、观察结果都打印，便于调试

## 运行（离线，无需 Key）

```bash
pip install -r requirements.txt
python examples/run.py
```

示例任务："北京时间现在几点，把 (23+19)*3 算出来，并查一下公司的退货政策"
→ Agent 依次调用 `now` / `calc` / `kb_search`，最后汇总成一段答复。

## 接真实大模型

```python
from agent.llm import AnthropicLLM
from agent.core import Agent
agent = Agent(llm=AnthropicLLM(model="claude-sonnet-5"))  # 需 ANTHROPIC_API_KEY
```

## 结构

```
agent/
  core.py     Agent 循环 + 工具调度
  llm.py      LLM 接口：MockLLM / AnthropicLLM
  tools.py    工具集（calc / now / kb_search）
  kb.py       知识库轻量检索
docs/         知识库文档
examples/run.py
```
