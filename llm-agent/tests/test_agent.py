import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent import Agent
from agent.tools import calc, kb_search


def test_calc_tool():
    assert calc("(23+19)*3") == "126"
    assert calc("100/4 + 6") == "31.0"


def test_kb_search_hits_policy():
    out = kb_search("退货")
    assert "7 天" in out


def test_agent_multistep():
    agent = Agent(verbose=False)
    res = agent.run("现在几点，算一下 (23+19)*3，并查退货政策")
    actions = [s["action"] for s in res["steps"]]
    assert actions == ["now", "calc", "kb_search"]
    assert "126" in res["answer"]
    assert "7 天" in res["answer"]
