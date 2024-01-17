"""empty message

Revision ID: 49d434a8c16a
Revises: 
Create Date: 2024-01-17 10:51:06.276097

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '49d434a8c16a'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('telegram_chat',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('chat_id', sa.BigInteger(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('telegram_message',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('message_id', sa.BigInteger(), nullable=True),
    sa.Column('chat_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['chat_id'], ['telegram_chat.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('category_hashtag',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('message_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['message_id'], ['telegram_message.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('hashtag',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('message_id', sa.Integer(), nullable=True),
    sa.Column('category_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['category_id'], ['category_hashtag.id'], ),
    sa.ForeignKeyConstraint(['message_id'], ['telegram_message.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('hashtag')
    op.drop_table('category_hashtag')
    op.drop_table('telegram_message')
    op.drop_table('telegram_chat')
    # ### end Alembic commands ###