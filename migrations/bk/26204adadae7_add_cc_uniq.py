"""add cc uniq

Revision ID: 26204adadae7
Revises: aca1e77c69ab
Create Date: 2023-07-24 02:28:51.714838

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '26204adadae7'
down_revision = 'aca1e77c69ab'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('choices', schema=None) as batch_op:
        batch_op.create_unique_constraint(None, ['is_correct'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('choices', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')

    # ### end Alembic commands ###
