"""empty message

Revision ID: af8bbbf2124a
Revises: e89c9c0da8de
Create Date: 2019-01-10 18:56:18.577523

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'af8bbbf2124a'
down_revision = 'e89c9c0da8de'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('notes', sa.Column('title', sa.String(length=128), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('notes', 'title')
    # ### end Alembic commands ###
