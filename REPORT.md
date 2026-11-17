# Проверка CHECK-ограничений (миграция) 
Миграция: `4de53981cf40` — `balance_is_positive`, `stock_is_positive`

Перед прогоном: `python setup.py`

## Тест 1: `proof_balance.py`

Команда: `python proof_balance.py`

Попытка: `UPDATE users SET balance = -1` без проверки в приложении.

Результат: **БД отказала**

Данные не изменились (commit не прошёл).

## Тест 2: `proof_stock.py`

Команда: `python proof_stock.py`

Попытка: `UPDATE products SET stock = -1` без проверки в приложении.

Результат: **БД отказала**

Данные не изменились (commit не прошёл).

## Итог

Оба скрипта падают с `IntegrityError` / `CheckViolation` — ограничения из миграции работают.

## После downgrade:
### Тест 1: `proof_balance.py`

(.venv) egor@DESKTOP-3E17JFI:~/x5_lab4$ alembic downgrade -1
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.runtime.migration] Running downgrade 4de53981cf40 -> , Добавляем ограничение в базу данных

(.venv) egor@DESKTOP-3E17JFI:~/x5_lab4$ python proof_balance.py
до: id=1 balance=100.00
ошибка: БД приняла отрицательный баланс

## Тест 2: `proof_stock.py`
(.venv) egor@DESKTOP-3E17JFI:~/x5_lab4$ python proof_stock.py
до: id=1 stock=100
ошибка: БД приняла отрицательный stock