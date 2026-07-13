"""配置：从环境变量读取 Ozon 凭证，缺失即启用 mock 模式。"""
from __future__ import annotations

import os


class Settings:
    ozon_client_id: str = os.environ.get("OZON_CLIENT_ID", "")
    ozon_api_key: str = os.environ.get("OZON_API_KEY", "")
    base_url: str = os.environ.get("OZON_BASE_URL", "https://api-seller.ozon.ru")

    @property
    def mock(self) -> bool:
        return not (self.ozon_client_id and self.ozon_api_key)


settings = Settings()
