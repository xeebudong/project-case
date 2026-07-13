"""BaseScraper：会话保持、重试、令牌桶限流、UA 轮换。"""
from __future__ import annotations

import random
import threading
import time
from dataclasses import dataclass, field

import requests

_UAS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
]


class RateLimiter:
    """简单令牌桶：每秒 `rate` 个请求。"""

    def __init__(self, rate: float = 3.0):
        self.rate = rate
        self._lock = threading.Lock()
        self._allowance = rate
        self._last = time.monotonic()

    def acquire(self) -> None:
        with self._lock:
            now = time.monotonic()
            self._allowance = min(self.rate, self._allowance + (now - self._last) * self.rate)
            self._last = now
            if self._allowance < 1.0:
                time.sleep((1.0 - self._allowance) / self.rate)
                self._allowance = 0.0
            else:
                self._allowance -= 1.0


@dataclass
class BaseScraper:
    base_url: str = ""
    rate: float = 3.0
    timeout: int = 20
    max_retries: int = 4
    session: requests.Session = field(default_factory=requests.Session)

    def __post_init__(self) -> None:
        self._limiter = RateLimiter(self.rate)
        self.session.headers.update({"Referer": self.base_url or "https://www.google.com/"})

    def get(self, url: str, **kw) -> requests.Response:
        last_exc = None
        for attempt in range(self.max_retries):
            self._limiter.acquire()
            self.session.headers["User-Agent"] = random.choice(_UAS)
            try:
                resp = self.session.get(url, timeout=self.timeout, **kw)
                if resp.status_code in (429, 503):
                    raise requests.HTTPError(f"throttled {resp.status_code}")
                resp.raise_for_status()
                return resp
            except requests.RequestException as e:  # noqa: PERF203
                last_exc = e
                time.sleep(min(2 ** attempt + random.random(), 30))
        raise RuntimeError(f"GET failed after {self.max_retries} tries: {url}") from last_exc

    def warmup(self, url: str) -> None:
        """预热：某些站点首访返回 JS 跳转并下发 Cookie，二次请求才拿到真页。"""
        try:
            self.get(url)
        except RuntimeError:
            pass
