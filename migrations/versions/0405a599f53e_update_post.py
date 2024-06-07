"""update post

Revision ID: 0405a599f53e
Revises: f8d3dc64f0e1
Create Date: 2024-06-07 12:31:06.117503

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '0405a599f53e'
down_revision = 'f8d3dc64f0e1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('post', sa.Column('user_id', sa.BINARY(length=16), nullable=False))
    op.create_foreign_key(op.f('fk_post_user_id_users'), 'post', 'users', ['user_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(op.f('fk_post_user_id_users'), 'post', type_='foreignkey')
    op.drop_column('post', 'user_id')
    # ### end Alembic commands ###
