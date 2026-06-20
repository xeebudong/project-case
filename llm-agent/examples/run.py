"""离线跑通 Agent：无需任何 API Key。"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent import Agent

if __name__ == "__main__":
    agent = Agent()
    tasks = [
        "北京时间现在几点，把 (23+19)*3 算出来，并查一下公司的退货政策",
        "帮我算 100/4 + 6，另外运费政策是怎样的",
    ]
    for t in tasks:
        print("=" * 60)
        agent.run(t)
