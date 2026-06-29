"""add description to todos

Revision ID: 0001_add_description_to_todos
Revises: 
Create Date: 2026-06-29 00:00:00.000000
"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "0001_add_description_to_todos"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("todos", sa.Column("description", sa.String(length=500), nullable=True))


def downgrade() -> None:
    op.drop_column("todos", "description")
