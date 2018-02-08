"""3/ Add bot managing game into game table

Revision ID: 64a92297f9a4
Revises: 03745d9649bb
Create Date: 2018-02-08 16:51:52.465502

"""

# revision identifiers, used by Alembic.
revision = '64a92297f9a4'
down_revision = '03745d9649bb'

from alembic import op
import sqlalchemy as sa


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('game', sa.Column('bot', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('game', 'bot')
    # ### end Alembic commands ###