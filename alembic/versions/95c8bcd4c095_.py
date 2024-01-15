"""empty message

Revision ID: 95c8bcd4c095
Revises: 7270f3249e44
Create Date: 2024-01-15 11:50:55.035720

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '95c8bcd4c095'
down_revision: Union[str, None] = '7270f3249e44'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('category_hashtag_hashtag_id_fkey', 'category_hashtag', type_='foreignkey')
    op.drop_column('category_hashtag', 'hashtag_id')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('category_hashtag', sa.Column('hashtag_id', sa.BIGINT(), autoincrement=False, nullable=True))
    op.create_foreign_key('category_hashtag_hashtag_id_fkey', 'category_hashtag', 'hashtag', ['hashtag_id'], ['id'])
    # ### end Alembic commands ###