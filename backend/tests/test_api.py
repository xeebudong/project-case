import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health():
    r = client.get("/api/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_summary_mock():
    r = client.get("/api/summary?days=7")
    assert r.status_code == 200
    body = r.json()
    assert body["gmv"] > 0
    assert body["orders"] > 0
    assert 0 <= body["active_sku_ratio"] <= 1


def test_top_skus():
    r = client.get("/api/top-skus?days=30&limit=5")
    assert r.status_code == 200
    rows = r.json()
    assert len(rows) == 5
    gmvs = [x["gmv"] for x in rows]
    assert gmvs == sorted(gmvs, reverse=True)
