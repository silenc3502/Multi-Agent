from typing import List, Optional
from datetime import datetime

from cart.domain.cart_item import CartItem


class Cart:
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.items: List[CartItem] = []
        self.created_at: datetime = datetime.utcnow()
        self.updated_at: datetime = datetime.utcnow()

    @classmethod
    def create(cls, user_id: str) -> "Cart":
        if not user_id:
            raise ValueError("User ID cannot be empty")
        return cls(user_id)

    def add_item(self, item: CartItem):
        # 실제 시스템은 중복 처리(동일 상품이면 수량 합침) 등을 여기에 둠
        # 간단히 동일 product_id이면 quantity 증가
        for existing in self.items:
            if existing.product_id == item.product_id:
                existing.quantity += item.quantity
                self.updated_at = datetime.utcnow()
                return
        self.items.append(item)
        self.updated_at = datetime.utcnow()

    def remove_item(self, product_id: str):
        self.items = [i for i in self.items if i.product_id != product_id]
        self.updated_at = datetime.utcnow()

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "items": [item.to_dict() for item in self.items]
        }
