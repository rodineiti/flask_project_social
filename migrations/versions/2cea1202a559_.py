"""empty message

Revision ID: 2cea1202a559
Revises: 3d305c64bccf
Create Date: 2018-07-26 09:51:49.270321

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2cea1202a559'
down_revision = '3d305c64bccf'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('comments', sa.Column('body', sa.Text(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('comments', 'body')
    # ### end Alembic commands ###
