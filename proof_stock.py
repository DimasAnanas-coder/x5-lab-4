"""Намеренно ставим stock < 0 без проверок в приложении. БД должна отказать."""
from db import SessionLocal
from models import Product
from sqlalchemy import update

with SessionLocal() as session:
    product = session.query(Product).first()
    if product is None:
        raise SystemExit("нет товаров — сначала python setup.py")
    print(f"до: id={product.id} stock={product.stock}")
    session.execute(
        update(Product).where(Product.id == product.id).values(stock=-1)
    )
    session.commit()
    print("ошибка: БД приняла отрицательный stock")
