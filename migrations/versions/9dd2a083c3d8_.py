"""empty message

Revision ID: 9dd2a083c3d8
Revises: 482dc05a1808
Create Date: 2018-07-19 12:27:57.940243

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9dd2a083c3d8'
down_revision = '482dc05a1808'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('image', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'image')
    # ### end Alembic commands ###
