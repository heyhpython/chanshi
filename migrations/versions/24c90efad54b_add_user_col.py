"""add user col

Revision ID: 24c90efad54b
Revises: 9b0785de152c
Create Date: 2020-12-16 15:00:05.493925

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '24c90efad54b'
down_revision = '9b0785de152c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('avatar', sa.TEXT(), nullable=True, comment='头像地址'))
    op.add_column('user', sa.Column('gender', sa.SMALLINT(), nullable=True, comment='用户性别'))
    op.add_column('user', sa.Column('mobile', sa.Integer(), nullable=True, comment='手机号'))
    op.alter_column('user', 'nick_name',
               existing_type=mysql.VARCHAR(length=64),
               comment='微信的用户昵称',
               existing_nullable=True)
    op.create_index(op.f('ix_user_mobile'), 'user', ['mobile'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_user_mobile'), table_name='user')
    op.alter_column('user', 'nick_name',
               existing_type=mysql.VARCHAR(length=64),
               comment=None,
               existing_comment='微信的用户昵称',
               existing_nullable=True)
    op.drop_column('user', 'mobile')
    op.drop_column('user', 'gender')
    op.drop_column('user', 'avatar')
    # ### end Alembic commands ###
