# -*- coding: utf-8 -*-
"""
弹幕分类器 —— 把抓取到的弹幕分到语义类别。
采用可解释的关键词 + 正则规则(可平滑替换为向量/大模型分类)。
类别: 好评 / 提问 / 纠错 / 情绪 / 垃圾广告 / 其他
"""
from __future__ import annotations
import json, re, argparse
from collections import Counter
from typing import Dict, List

RULES = [
    ("垃圾广告", [r"加(微信|vx|qq)", r"出售", r"代刷", r"优惠券", r"广告"]),
    ("提问",   [r"[吗嘛]？?$", r"怎么", r"能不能", r"求.*源码", r"如何", r"\?$", r"？$"]),
    ("纠错",   [r"错(了|误)", r"应该是", r"不对", r"bug", r"有问题"]),
    ("好评",   [r"太.*了", r"讲得?清楚", r"学到了", r"感谢", r"神仙", r"yyds", r"nb"]),
    ("情绪",   [r"哈哈+", r"awsl", r"笑死", r"可爱", r"啊+", r"泪目"]),
]


def classify_one(text: str) -> str:
    for label, pats in RULES:
        for p in pats:
            if re.search(p, text, re.I):
                return label
    return "其他"


def classify(items: List[Dict]) -> List[Dict]:
    for it in items:
        it["category"] = classify_one(it.get("text", ""))
    return items


def main():
    ap = argparse.ArgumentParser(description="弹幕分类器")
    ap.add_argument("--in", dest="inp", default="danmu.json")
    ap.add_argument("--out", default="danmu_classified.json")
    args = ap.parse_args()

    items = json.load(open(args.inp, encoding="utf-8"))
    items = classify(items)
    json.dump(items, open(args.out, "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)

    dist = Counter(it["category"] for it in items)
    print(f"分类完成 {len(items)} 条 -> {args.out}")
    for k, v in dist.most_common():
        print(f"  {k:>6}: {v}")


if __name__ == "__main__":
    main()
