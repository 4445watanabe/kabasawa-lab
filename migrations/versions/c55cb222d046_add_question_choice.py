"""add question choice

Revision ID: c55cb222d046
Revises: e2ccc256a6b5
Create Date: 2023-07-10 07:37:43.830963

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c55cb222d046'
down_revision = 'e2ccc256a6b5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('questions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('question_text', sa.String(length=128), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('question_text')
    )
    op.create_table('choice',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('question_id', sa.Integer(), nullable=True),
    sa.Column('choice_text', sa.String(length=128), nullable=False),
    sa.Column('is_correct', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['question_id'], ['questions.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('choice_text')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('choice')
    op.drop_table('questions')
    # ### end Alembic commands ###
