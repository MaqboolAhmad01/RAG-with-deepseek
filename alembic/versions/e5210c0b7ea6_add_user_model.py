"""Add_user_model

Revision ID: e5210c0b7ea6
Revises: 4dd1fdd006f8
Create Date: 2025-07-06 16:37:06.199724

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e5210c0b7ea6'
down_revision: Union[str, None] = '4dd1fdd006f8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users', sa.Column('username', sa.String(), nullable=True))
    op.add_column('users', sa.Column('profile_pic', sa.String(), nullable=True))
    op.add_column('users', sa.Column('about', sa.String(), nullable=True))


def downgrade() -> None:
    op.drop_column('users', 'about')
    op.drop_column('users', 'profile_pic')
    op.drop_column('users', 'username')