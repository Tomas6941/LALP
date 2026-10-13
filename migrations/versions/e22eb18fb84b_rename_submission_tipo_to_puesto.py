"""rename submission tipo to puesto

Revision ID: e22eb18fb84b
Revises: 1894a2e3a13e
Create Date: 2026-10-13 08:36:49.561257

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e22eb18fb84b'
down_revision = '1894a2e3a13e'
branch_labels = None
depends_on = None


def upgrade():
    # Rename preserves existing values; batch mode maps to
    # ALTER TABLE ... RENAME COLUMN on SQLite.
    with op.batch_alter_table('submission', schema=None) as batch_op:
        batch_op.alter_column(
            'tipo',
            new_column_name='puesto',
            existing_type=sa.String(length=20),
            type_=sa.String(length=40),
            existing_nullable=False,
            nullable=False,
        )


def downgrade():
    with op.batch_alter_table('submission', schema=None) as batch_op:
        batch_op.alter_column(
            'puesto',
            new_column_name='tipo',
            existing_type=sa.String(length=40),
            type_=sa.VARCHAR(length=20),
            existing_nullable=False,
            nullable=False,
        )
