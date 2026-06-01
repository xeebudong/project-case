from ecom_scraper.adapters.demo import DemoAdapter
from ecom_scraper.pipeline import run


def test_demo_dedup():
    items = run(DemoAdapter(seed=1), pages=3)
    keys = [it["sku"] for it in items]
    assert len(keys) == len(set(keys)) == 60


def test_rate_limiter_smoke():
    from ecom_scraper.base import RateLimiter
    rl = RateLimiter(rate=1000)
    for _ in range(10):
        rl.acquire()
