"""Добавляем ограничение в базу данных

Revision ID: 4de53981cf40
Revises: 
Create Date: 2026-11-17 18:52:40.327020

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4de53981cf40'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_check_constraint("balance_is_positive", "users", "balance >= 0")
    op.create_check_constraint("stock_is_positive", "products", "stock >= 0")


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint("balance_is_positive", "users", type_="check")
    op.drop_constraint("stock_is_positive", "products", type_="check")
