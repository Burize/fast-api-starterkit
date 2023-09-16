"""add order model

Revision ID: 09dd2f758b32
Revises: eaf64d90c86b
Create Date: 2023-09-16 23:38:47.197170

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '09dd2f758b32'
down_revision = 'eaf64d90c86b'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute('CREATE SEQUENCE store_order_number_seq')

    op.create_table('store_order',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('number', sa.Integer(), server_default=sa.text("nextval('store_order_number_seq'::regclass)"), nullable=False),
    sa.Column('description', sa.Text(), nullable=False),
    sa.Column('user_id', sa.UUID(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['auth_user.id'], name=op.f('fk_store_order_user_id'), ondelete='CASCADE', initially='DEFERRED', deferrable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_store_order')),
    sa.UniqueConstraint('number', name=op.f('uq_store_order_number'))
    )


def downgrade() -> None:
    op.drop_table('store_order')
    op.execute('DROP SEQUENCE store_order_number_seq')

