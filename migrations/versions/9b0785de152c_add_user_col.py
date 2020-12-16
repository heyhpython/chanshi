"""add user col

Revision ID: 9b0785de152c
Revises: e77610888417
Create Date: 2020-12-15 19:08:04.790795

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9b0785de152c'
down_revision = 'e77610888417'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('openid', sa.String(length=64), nullable=True, comment='用户唯一标识'))
    op.add_column('user', sa.Column('unionid', sa.String(length=64), nullable=True, comment='开放平台唯一id'))
    op.create_index(op.f('ix_user_openid'), 'user', ['openid'], unique=True)
    op.create_index(op.f('ix_user_unionid'), 'user', ['unionid'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_user_unionid'), table_name='user')
    op.drop_index(op.f('ix_user_openid'), table_name='user')
    op.drop_column('user', 'unionid')
    op.drop_column('user', 'openid')
    # ### end Alembic commands ###
