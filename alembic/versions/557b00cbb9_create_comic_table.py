"""Create comic table

Revision ID: 557b00cbb9
Revises: 
Create Date: 2015-07-31 19:25:14.508177

"""

# revision identifiers, used by Alembic.
revision = '557b00cbb9'
down_revision = None
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table('comic',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('month', sa.String(), nullable=True),
                    sa.Column('num', sa.Integer(), nullable=False),
                    sa.Column('link', sa.String(), nullable=True),
                    sa.Column('year', sa.String(), nullable=True),
                    sa.Column('news', sa.String(), nullable=True),
                    sa.Column('safe_title', sa.String(), nullable=False),
                    sa.Column('transcript', sa.String(), nullable=True),
                    sa.Column('alt', sa.String(), nullable=True),
                    sa.Column('img', sa.String(), nullable=True),
                    sa.Column('title', sa.String(), nullable=True),
                    sa.Column('day', sa.String(), nullable=True),
                    sa.PrimaryKeyConstraint('id')
                    )


def downgrade():
    op.drop_table('comic')
