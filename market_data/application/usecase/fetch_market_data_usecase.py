# application/usecase/fetch_market_data_usecase.py
from typing import List
from datetime import datetime
from ...application.port.market_data_api_port import MarketDataAPIPort
from ...application.dto.market_item_dto import MarketItemDTO
from ...domain.market_item import MarketItem
from ...domain.value_object.market_price import MarketPrice
from ...domain.value_object.timestamp import Timestamp
from ...domain.market_data import MarketData

class FetchMarketDataUsecase:
    def __init__(self, api_port: MarketDataAPIPort):
        self.api_port = api_port

    async def execute(self, query: str) -> MarketData:
        dtos: List[MarketItemDTO] = await self.api_port.fetch_market_data(query)
        items: List[MarketItem] = [
            MarketItem(
                name=dto.name,
                price=MarketPrice(dto.price),      # VO 사용
                timestamp=Timestamp(datetime.now()) # VO 사용
            )
            for dto in dtos
        ]
        return MarketData(items=items, source="NaverAPI", fetched_at=datetime.now())
