from fastapi import APIRouter, Request, Cookie, HTTPException, Depends

from cart.application.usecase.cart_usecase import CartUseCaseImpl
from utility.session_helper import get_current_user

cart_router = APIRouter()
cart_usecase = CartUseCaseImpl()


@cart_router.get("/list")
async def get_cart(user_id: str = Depends(get_current_user)):
    cart = await cart_usecase.get_cart(user_id)
    return cart


@cart_router.post("/add")
async def add_to_cart(product_id: str, user_id: str = Depends(get_current_user)):
    cart = await cart_usecase.get_cart(user_id)
    products = await cart_usecase.search_products(product_id)
    if products:
        await cart_usecase.add_to_cart(cart, products[0], user_id)
    return await cart_usecase.get_cart(user_id)
