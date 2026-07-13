# -*- coding: utf-8 -*-
"""ecom-api-adapter 的自测：三平台样例订单 -> 统一模型。"""
import json, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
from adapter import normalize_batch

SAMPLE = {
    "ozon": [{
        "posting_number": "0001-0002-1", "status": "awaiting_packaging",
        "currency_code": "CNY", "in_process_at": 1650000000,
        "customer": {"name": "Ivan"},
        "products": [{"sku": "A100", "name": "保温杯", "quantity": 2, "price": 59.0}],
    }],
    "shopify": [{
        "name": "#1001", "financial_status": "paid", "currency": "USD",
        "total_price": "42.00", "created_at": "2026-07-01T08:00:00Z",
        "customer": {"first_name": "Anna"},
        "line_items": [{"sku": "B200", "title": "Serum", "quantity": 1, "price": "42.00"}],
    }],
    "pdd": [{
        "order_sn": "PDD202607130001", "order_status": 2, "order_amount": 3980,
        "created_time": 1650003600, "receiver_name": "王先生",
        "item_list": [{"goods_id": "C300", "goods_name": "手机壳",
                       "goods_count": 1, "goods_price": 3980}],
    }],
}


def main():
    rows = normalize_batch(SAMPLE)
    assert len(rows) == 3
    by = {r["platform"]: r for r in rows}
    assert by["ozon"]["status"] == "paid"
    assert by["ozon"]["total"] == 118.0
    assert by["shopify"]["status"] == "paid"
    assert by["pdd"]["status"] == "paid"
    assert by["pdd"]["total"] == 39.8
    print("✅ 全部断言通过，统一订单输出：")
    print(json.dumps(rows, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
