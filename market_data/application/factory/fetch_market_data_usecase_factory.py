from ...infrastructure.api.market_data_api_adapter import MarketDataAPIAdapter
from ..usecase.fetch_market_data_usecase import FetchMarketDataUsecase

class FetchMarketDataUsecaseFactory:
    @staticmethod
    def create() -> FetchMarketDataUsecase:
        api_adapter = MarketDataAPIAdapter()
        return FetchMarketDataUsecase(api_adapter)
