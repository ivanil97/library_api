"""user model corrected

Revision ID: b9b83f6bb242
Revises: 07e1d6f84813
Create Date: 2025-01-20 23:24:46.533067

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b9b83f6bb242'
down_revision: Union[str, None] = '07e1d6f84813'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'password',
               existing_type=sa.VARCHAR(length=100),
               type_=sa.String(length=1000),
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'password',
               existing_type=sa.String(length=1000),
               type_=sa.VARCHAR(length=100),
               existing_nullable=True)
    # ### end Alembic commands ###
