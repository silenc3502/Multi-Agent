# infrastructure/api/market_data_api_adapter.py
import os
import aiohttp
from typing import List
from ...application.dto.market_item_dto import MarketItemDTO
from ...application.port.market_data_api_port import MarketDataAPIPort
from urllib.parse import quote

class MarketDataAPIAdapter(MarketDataAPIPort):
    NAVER_CLIENT_ID = os.getenv("NAVER_CLIENT_ID")
    NAVER_CLIENT_SECRET = os.getenv("NAVER_CLIENT_SECRET")

    async def fetch_market_data(self, query: str) -> List[MarketItemDTO]:
        encoded_query = quote(query)  # 한글 인코딩
        url = f"https://openapi.naver.com/v1/search/shop.json?query={encoded_query}&display=10"

        headers = {
            "X-Naver-Client-Id": self.NAVER_CLIENT_ID,
            "X-Naver-Client-Secret": self.NAVER_CLIENT_SECRET,
        }
        print(f"headers: {headers}")

        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as resp:
                print("HTTP Status:", resp.status)
                raw_text = await resp.text()
                print("Raw Response Text:", raw_text)

                if resp.status != 200:
                    raise Exception(f"Naver API Error {resp.status}")

                data = await resp.json()
                print("Parsed JSON:", data)

        return [
            MarketItemDTO(
                name=entry.get("title", ""),
                price=int(entry.get("lprice", 0))
            )
            for entry in data.get("items", [])
        ]
