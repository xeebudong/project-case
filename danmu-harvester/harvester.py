# -*- coding: utf-8 -*-
"""
danmu-harvester —— 弹幕数据抓取器

支持从 B 站视频的 cid 拉取弹幕 XML 并解析为结构化记录。
离线模式(--sample)使用内置样例，无需网络即可演示完整 pipeline。
"""
from __future__ import annotations
import argparse, re, sys, json, xml.etree.ElementTree as ET
from dataclasses import dataclass, asdict
from typing import List

try:
    import urllib.request
except Exception:  # pragma: no cover
    urllib = None

DANMU_API = "https://comment.bilibili.com/{cid}.xml"

SAMPLE_XML = """<?xml version="1.0"?><i>
<d p="4.12,1,25,16777215,1650000000,0,abc,1">前排！这个讲得太清楚了</d>
<d p="9.30,1,25,16777215,1650000001,0,def,2">哈哈哈哈哈笑死我了</d>
<d p="15.0,5,25,16711680,1650000002,0,ghi,3">up主能出个源码吗求求了</d>
<d p="21.7,1,25,16777215,1650000003,0,jkl,4">这里有个错误吧？应该是 O(n) 才对</d>
<d p="30.2,1,25,16777215,1650000004,0,mno,5">awsl 太可爱了</d>
<d p="41.9,1,25,16777215,1650000005,0,pqr,6">广告加微信 xxx 出售各种课程</d>
<d p="52.1,1,25,16777215,1650000006,0,stu,7">感谢分享，学到了！</d>
</i>"""


@dataclass
class Danmu:
    time: float          # 出现时间(秒)
    mode: int            # 弹幕类型
    fontsize: int
    color: int
    ts: int              # 发送时间戳
    text: str


def parse_xml(xml_text: str) -> List[Danmu]:
    root = ET.fromstring(xml_text)
    out: List[Danmu] = []
    for d in root.findall("d"):
        p = (d.get("p") or "").split(",")
        if len(p) < 5:
            continue
        out.append(Danmu(
            time=float(p[0]), mode=int(p[1]), fontsize=int(p[2]),
            color=int(p[3]), ts=int(p[4]), text=(d.text or "").strip(),
        ))
    return out


def fetch(cid: str) -> str:
    url = DANMU_API.format(cid=cid)
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=15) as r:
        raw = r.read()
    return raw.decode("utf-8", "ignore")


def main():
    ap = argparse.ArgumentParser(description="B 站弹幕抓取器")
    ap.add_argument("--cid", help="视频 cid")
    ap.add_argument("--sample", action="store_true", help="使用内置样例(离线)")
    ap.add_argument("--out", default="danmu.json", help="输出 JSON 路径")
    args = ap.parse_args()

    if args.sample:
        xml_text = SAMPLE_XML
    elif args.cid:
        xml_text = fetch(args.cid)
    else:
        ap.error("需要 --cid 或 --sample")

    items = parse_xml(xml_text)
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump([asdict(x) for x in items], f, ensure_ascii=False, indent=2)
    print(f"抓取 {len(items)} 条弹幕 -> {args.out}")


if __name__ == "__main__":
    main()
