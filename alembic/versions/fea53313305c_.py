"""empty message

Revision ID: fea53313305c
Revises: 973bc56323ec
Create Date: 2024-01-08 22:42:11.769611

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fea53313305c'
down_revision: Union[str, None] = '973bc56323ec'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('admin_chat')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('admin_chat',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('admin_user', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('chat_id', sa.BIGINT(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['chat_id'], ['telegram_chat.id'], name='admin_chat_chat_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='admin_chat_pkey')
    )
    # ### end Alembic commands ###
