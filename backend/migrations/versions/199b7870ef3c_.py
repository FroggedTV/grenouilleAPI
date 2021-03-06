"""3/ Add dota items and dota heroes

Revision ID: 199b7870ef3c
Revises: 0d4fdbeccbf8
Create Date: 2018-08-11 13:55:57.881258

"""

# revision identifiers, used by Alembic.
revision = '199b7870ef3c'
down_revision = '0d4fdbeccbf8'

from alembic import op
import sqlalchemy as sa


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('dota_heroes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.Text(), nullable=False),
    sa.Column('short_name', sa.Text(), nullable=False),
    sa.Column('localized_name', sa.Text(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('dota_items',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.Text(), nullable=False),
    sa.Column('short_name', sa.Text(), nullable=False),
    sa.Column('localized_name', sa.Text(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('dota_items')
    op.drop_table('dota_heroes')
    # ### end Alembic commands ###
