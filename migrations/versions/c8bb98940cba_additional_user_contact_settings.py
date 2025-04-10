"""additional user & contact settings

Revision ID: c8bb98940cba
Revises: 
Create Date: 2025-04-10 11:17:38.325735

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c8bb98940cba'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('contacts', schema=None) as batch_op:
        batch_op.alter_column('phone',
               existing_type=sa.VARCHAR(),
               nullable=True)

    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('smtp_server', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('smtp_port', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('imap_server', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('imap_port', sa.Integer(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('imap_port')
        batch_op.drop_column('imap_server')
        batch_op.drop_column('smtp_port')
        batch_op.drop_column('smtp_server')

    with op.batch_alter_table('contacts', schema=None) as batch_op:
        batch_op.alter_column('phone',
               existing_type=sa.VARCHAR(),
               nullable=False)

    # ### end Alembic commands ###
