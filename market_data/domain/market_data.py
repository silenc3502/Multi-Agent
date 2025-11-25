from .entity.market_item import MarketItem
from datetime import datetime
from typing import List

class MarketData:
    def __init__(self, items: List[MarketItem], source: str, fetched_at: datetime):
        self.items = items
        self.source = source
        self.fetched_at = fetched_at

    def add_item(self, item: MarketItem):
        self.items.append(item)
