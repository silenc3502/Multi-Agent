from market_data.domain.value_object.market_price import MarketPrice
from market_data.domain.value_object.timestamp import Timestamp


class MarketItem:
    def __init__(self, name: str, price: MarketPrice, timestamp: Timestamp):
        self.name = name
        self.price = price
        self.timestamp = timestamp
