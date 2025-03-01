"""
Протестируйте классы из модуля homework/models.py
"""

import pytest

from homework.models import Product
from homework.models import Cart


@pytest.fixture
def product():
    return Product("book", 100, "This is a book", 1000)


@pytest.fixture
def pen():
    return Product("pen", 20, "This is a pen", 500)


@pytest.fixture
def cart():
    return Cart()


class TestProducts:
    """
    Тестовый класс - это способ группировки ваших тестов по какой-то тематике
    Например, текущий класс группирует тесты на класс Product
    """

    def test_product_check_quantity(self, product):
        # TODO напишите проверки на метод check_quantity
        assert product.check_quantity(0) == True  # 0 можно "купить"
        assert product.check_quantity(1) == True  # Минимальное возможное количество
        assert product.check_quantity(1000) == True  # Ровно столько, сколько есть
        assert product.check_quantity(1001) == False  # На 1 больше, чем есть

    def test_product_buy(self, product):
        # TODO напишите проверки на метод buy
        product.buy(10)
        assert product.quantity == 990

    def test_product_buy_more_than_available(self, product):
        # TODO напишите проверки на метод buy,
        #  которые ожидают ошибку ValueError при попытке купить больше, чем есть в наличии
        with pytest.raises(ValueError):
            product.buy(product.quantity + 2)


class TestCart:

    def test_add_product(self, cart, product, pen):
        cart.add_product(product, 2)
        cart.add_product(pen, 2)
        assert cart.products[product] == 2
        assert cart.products[pen] == 2

    def test_add_same_product_increases(self, cart, product):
        cart.add_product(product, 2)
        cart.add_product(product, 5)
        assert cart.products[product] == 7

    def test_remove_product(self, cart, product):
        cart.add_product(product, 10)
        cart.remove_product(product, 3)
        assert cart.products[product] == 7

    def test_remove_allproduct(self, cart, product):
        cart.add_product(product, 10)
        cart.remove_product(product, 10)
        assert product not in cart.products

    def test_remove_more_products(self, cart, product):
        cart.add_product(product, 5)
        cart.remove_product(product, 6)
        assert product not in cart.products

    def test_get_total(self, cart, product, pen):
        cart.add_product(product, 5)
        cart.add_product(pen, 3)
        assert cart.get_total_price() == (5 * product.price) + (3 * pen.price)

    def test_clear_cart(self, cart, product, pen):
        cart.add_product(product, 3)
        cart.add_product(pen, 2)
        cart.clear()
        assert not cart.products

    def test_cart_buy_success(self, cart, product, pen):
        cart.add_product(product, 2)
        cart.add_product(pen, 4)
        cart.buy()
        assert product.quantity == 998
        assert pen.quantity == 496
        assert not cart.products

    def test_cart_buy_not_enough_stock(self, cart, product):
        cart.add_product(product, 1001)
        with pytest.raises(ValueError, match="Product 'book' is out of stock"):
            cart.buy()

    def test_get_total_after_buy(self, cart, product):
        cart.add_product(product, 3)
        cart.buy()
        assert cart.get_total_price() == 0

    def test_add_negative_quantity(self, cart, product):
        with pytest.raises(ValueError, match="Product quantity must be positive"):
            cart.add_product(product, -3)
