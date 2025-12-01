from cart.domain.cart import Cart
from cart.domain.cart_item import CartItem
from cart.domain.value_object.price import Price
from cart.infrastructure.repository.cart_repository_impl import CartRepositoryImpl
from cart.infrastructure.repository.cart_item_repository_impl import CartItemRepositoryImpl

class CartUseCaseImpl:
    def __init__(self):
        self.cart_repo = CartRepositoryImpl()
        self.cart_item_repo = CartItemRepositoryImpl()

    async def get_cart(self, user_id: int) -> Cart:
        """
        유저의 카트를 조회합니다. 없으면 새로 생성합니다.
        """
        cart = self.cart_repo.find_by_account_id(user_id)
        if cart is None:
            cart = Cart(account_id=user_id)
            cart = self.cart_repo.save(cart)
        return cart

    async def add_to_cart(self, cart: Cart, product: dict, user_id: int):
        """
        Cart에 상품 추가. product dict는 Router에서 market-data로부터 전달받습니다.
        """
        # 상품 정보 추출
        product_id = product.get("id")  # market-data에서 넘어온 id
        price_value = int(product.get("price", 0))
        quantity = 1  # 기본 수량 1, 필요시 Router에서 받아서 확장 가능

        # CartItem 생성
        item = CartItem(cart_id=cart.id, product_id=product_id, quantity=quantity, price=Price(price_value))
        self.cart_item_repo.save(item)
