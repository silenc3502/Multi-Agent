from datetime import datetime

class PromotionService:
    def __init__(self, discount: float, start_time: datetime, end_time: datetime):
        self.discount = discount
        self.start_time = start_time
        self.end_time = end_time

    def is_active(self, current_time: datetime = None) -> bool:
        now = current_time or datetime.now()
        return self.start_time <= now <= self.end_time

    def apply_discount(self, price: float, current_time: datetime = None) -> float:
        if self.is_active(current_time):
            return price * (1 - self.discount)
        return price
