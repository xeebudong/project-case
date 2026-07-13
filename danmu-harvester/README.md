# danmu-harvester · 弹幕数据抓取与分类

一条完整的 **抓取 → 结构化 → 语义分类** pipeline。

## 能力
- `harvester.py`：从 B 站 `cid` 拉取弹幕 XML，解析为结构化记录（时间/类型/颜色/时间戳/文本）。带 `--sample` 离线样例，开箱即跑。
- `classifier.py`：可解释的关键词 + 正则分类器，把弹幕分到 **好评 / 提问 / 纠错 / 情绪 / 垃圾广告 / 其他**；规则层可无缝替换为向量检索或大模型分类。

## 快速开始
```bash
# 离线样例跑通全流程
python harvester.py --sample --out danmu.json
python classifier.py --in danmu.json --out danmu_classified.json

# 真实抓取(需 cid)
python harvester.py --cid 123456789 --out danmu.json
```

## 输出示例
```
分类完成 7 条 -> danmu_classified.json
    好评: 3
    提问: 1
    纠错: 1
    情绪: 1
  垃圾广告: 1
```

## 工程化扩展点
- 增量抓取 + 去重（按 `ts` + 文本 hash）
- 分类器换成 fastText / BGE 向量 + 阈值，或直接调大模型批量打标
- 落库 DuckDB / Parquet，接可视化看板
