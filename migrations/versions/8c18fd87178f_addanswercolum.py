"""addanswerColum

Revision ID: 8c18fd87178f
Revises: 454e682618e4
Create Date: 2023-07-24 01:59:18.536425

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8c18fd87178f'
down_revision = '454e682618e4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('choices', schema=None) as batch_op:
        batch_op.add_column(sa.Column('choice_answer', sa.Boolean(), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('choices', schema=None) as batch_op:
        batch_op.drop_column('choice_answer')

    # ### end Alembic commands ###