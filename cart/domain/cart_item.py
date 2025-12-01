from datetime import datetime
from typing import Dict, Any

from cart.domain.value_object.price import Price


class CartItem:
    def __init__(self, product_id: str, name: str, price: Price, quantity: int = 1):
        if not product_id:
            raise ValueError("product_id required")
        if not name:
            raise ValueError("name required")
        if quantity <= 0:
            raise ValueError("quantity must be >= 1")

        self.product_id = str(product_id)
        self.name = name
        self.price = price
        self.quantity = quantity
        self.added_at = datetime.utcnow()

    @classmethod
    def create(cls, product_id: str, name: str, value: float, currency: str = "KRW", quantity: int = 1) -> "CartItem":
        price = Price(value, currency)
        return cls(product_id=product_id, name=name, price=price, quantity=quantity)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.product_id,
            "name": self.name,
            "price": self.price.to_dict(),
            "quantity": self.quantity,
            "added_at": self.added_at.isoformat()
        }
