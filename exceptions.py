"""Доменные ошибки сервиса заказов."""


class OutOfStockError(Exception):
    """Товара нет в наличии."""


class InsufficientFundsError(Exception):
    """Недостаточно средств на балансе."""


class ConflictError(Exception):
    """Конфликт: строку уже меняет другая транзакция."""

    code = 409

    def __init__(self, message="Конфликт параллельного изменения"):
        self.message = message
        super().__init__(message)
