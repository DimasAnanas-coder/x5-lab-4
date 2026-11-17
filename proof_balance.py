"""Намеренно ставим balance < 0 без проверок в приложении. БД должна отказать."""
from db import SessionLocal
from models import User
from sqlalchemy import update

with SessionLocal() as session:
    user = session.query(User).first()
    if user is None:
        raise SystemExit("нет пользователей — сначала python setup.py")
    print(f"до: id={user.id} balance={user.balance}")
    session.execute(
        update(User).where(User.id == user.id).values(balance=-1)
    )
    session.commit()
    print("ошибка: БД приняла отрицательный баланс")
