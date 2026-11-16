"""Дано: атомарный create_order уровня вашего ДЗ.
Одна транзакция, откат при сбое — против СБОЯ он корректен.
Против КОНКУРЕНЦИИ — нет. Это вы и исследуете. Правите только этот файл.
"""
from sqlalchemy import update
from sqlalchemy.exc import OperationalError
from models import User, Product, Order
from exceptions import OutOfStockError, InsufficientFundsError, ConflictError


def create_order(session, user_id, product_id):
    with session.begin():
        try:
            user = session.get(User, user_id, with_for_update={"nowait": True})
            product = session.get(Product, product_id, with_for_update={"nowait": True})
        except OperationalError as e:
            raise ConflictError("Строка занята другой транзакцией") from e

        if user is None:
            raise LookupError("Пользователь не найден")
        if product is None:
            raise LookupError("Товар не найден")
        price = product.price

        stock_result = session.execute(
            update(Product)
            .where(Product.id == product_id, Product.stock > 0)
            .values(stock=Product.stock - 1),
            execution_options={"synchronize_session": False},
        )
        if stock_result.rowcount != 1:
            raise OutOfStockError("Товара нет в наличии")

        balance_result = session.execute(
            update(User)
            .where(User.id == user_id, User.balance >= price)
            .values(balance=User.balance - price),
            execution_options={"synchronize_session": False},
        )
        if balance_result.rowcount != 1:
            raise InsufficientFundsError("Недостаточно средств")

        session.add(Order(user_id=user_id, product_id=product_id, amount=price))
