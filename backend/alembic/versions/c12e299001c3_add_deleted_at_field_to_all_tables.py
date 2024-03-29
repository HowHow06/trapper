"""add deleted_at field to all tables

Revision ID: c12e299001c3
Revises: 9634497e7435
Create Date: 2023-06-27 16:22:59.978660

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision = 'c12e299001c3'
down_revision = '9634497e7435'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('lookup', sa.Column('deleted_at', sa.DateTime(), nullable=True))
    op.add_column('result', sa.Column('deleted_at', sa.DateTime(), nullable=True))
    op.add_column('scan_request', sa.Column('deleted_at', sa.DateTime(), nullable=True))
    op.add_column('task', sa.Column('deleted_at', sa.DateTime(), nullable=True))
    op.add_column('user', sa.Column('deleted_at', sa.DateTime(), nullable=True))
    op.add_column('vulnerability', sa.Column('deleted_at', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('vulnerability', 'deleted_at')
    op.drop_column('user', 'deleted_at')
    op.drop_column('task', 'deleted_at')
    op.drop_column('scan_request', 'deleted_at')
    op.drop_column('result', 'deleted_at')
    op.drop_column('lookup', 'deleted_at')
    # ### end Alembic commands ###
