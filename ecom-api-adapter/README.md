# ecom-api-adapter · 多平台电商订单归一化中间件

把 **Ozon / Shopify / 拼多多** 等平台字段各异的订单，统一映射为内部标准模型
`UnifiedOrder`，屏蔽上游差异，下游二开只面向一套 schema。

## 设计
- `ADAPTERS` 注册表：每个平台一个 `from_xxx(raw) -> UnifiedOrder` 纯函数，新增平台只加一个适配器。
- `STATUS_MAP`：各平台订单状态 → 统一状态机（created/paid/shipped/done/cancelled）。
- 金额单位归一（拼多多以分计 → 元）、时间统一 ISO8601、货币字段保留。
- 零依赖，纯标准库，易单测、易嵌入任何后端。

## 运行自测
```bash
python test_adapter.py
# ✅ 全部断言通过，统一订单输出：...
```

## 接真实接口时
- 各平台 SDK / OpenAPI 拉单 → 丢给 `normalize(platform, raw)`
- 加签名鉴权、限流重试、Webhook 增量、幂等去重
- `normalize_batch()` 支持多平台批量拉取后统一入库
