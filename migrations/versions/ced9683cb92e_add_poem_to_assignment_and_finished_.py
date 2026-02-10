"""Add poem to assignment and finished flag to event

Revision ID: ced9683cb92e
Revises: 0af4df0f928c
Create Date: 2026-01-22 15:44:17.449083
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ced9683cb92e'
down_revision = '0af4df0f928c'
branch_labels = None
depends_on = None


def upgrade():

    # SQLite-safe table recreation
    with op.batch_alter_table('assignments', recreate='always') as batch_op:
        batch_op.add_column(sa.Column('poem', sa.Text(), nullable=True))

    with op.batch_alter_table('events', recreate='always') as batch_op:
        batch_op.add_column(sa.Column('is_finished', sa.Boolean(), nullable=False, server_default=sa.false()))


def downgrade():

    with op.batch_alter_table('events', recreate='always') as batch_op:
        batch_op.drop_column('is_finished')

    with op.batch_alter_table('assignments', recreate='always') as batch_op:
        batch_op.drop_column('poem')
