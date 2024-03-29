"""change result payload to text

Revision ID: c19bce2864ec
Revises: ccb1bb4d74f3
Create Date: 2023-07-10 13:46:03.293924

"""
import sqlalchemy as sa
import sqlmodel
from alembic import op
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'c19bce2864ec'
down_revision = 'ccb1bb4d74f3'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('result', 'payload',
                    existing_type=mysql.VARCHAR(length=255),
                    type_=mysql.TEXT(),
                    nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('result', 'payload',
                    existing_type=mysql.TEXT(),
                    type_=mysql.VARCHAR(length=255),
                    nullable=False)
    # ### end Alembic commands ###
