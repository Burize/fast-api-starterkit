"""add unique indexes to user model

Revision ID: eaf64d90c86b
Revises: 3f059a73ac6d
Create Date: 2023-09-15 19:46:24.611115

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'eaf64d90c86b'
down_revision = '3f059a73ac6d'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_index('ix_uq_auth_user_email', 'auth_user', [sa.text('lower(email)')], unique=True)
    op.create_unique_constraint(op.f('uq_auth_user_username'), 'auth_user', ['username'])


def downgrade() -> None:
    op.drop_constraint(op.f('uq_auth_user_username'), 'auth_user', type_='unique')
    op.drop_index('ix_uq_auth_user_email', table_name='auth_user')
