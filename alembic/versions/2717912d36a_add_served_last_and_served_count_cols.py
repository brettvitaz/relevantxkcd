"""Add served_last and served_count cols

Revision ID: 2717912d36a
Revises: 557b00cbb9
Create Date: 2015-08-06 07:58:56.070311

"""

# revision identifiers, used by Alembic.
revision = '2717912d36a'
down_revision = '557b00cbb9'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa

comic_table = sa.Table(
    'comic', sa.MetaData(),
    sa.Column('served_count', sa.Integer, nullable=False)
)


def upgrade():
    op.add_column('comic', sa.Column('served_count', sa.Integer(), nullable=False, server_default=sa.DefaultClause('0')))
    op.add_column('comic', sa.Column('served_last', sa.DateTime(), nullable=True))


def downgrade():
    op.create_table('comic_backup',
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

    op.execute('INSERT INTO comic_backup SELECT id,month,num,link,year,news,safe_title,transcript,alt,img,title,day FROM comic;')
    op.execute('DROP TABLE comic;')
    op.execute('ALTER TABLE comic_backup RENAME TO comic;')
