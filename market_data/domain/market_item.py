from ..value_object.market_price import MarketPrice
from ..value_object.timestamp_vo import TimestampVO

class MarketItem:
    def __init__(self, name: str, price: MarketPrice, timestamp: TimestampVO):
        self.name = name
        self.price = price
        self.timestamp = timestamp
