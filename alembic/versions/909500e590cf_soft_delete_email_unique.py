"""soft_delete_email_unique

Revision ID: 909500e590cf
Revises: 217426ce67f2
Create Date: 2026-03-17 13:32:13.092305

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '909500e590cf'
down_revision: Union[str, Sequence[str], None] = '217426ce67f2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None: # Enforce unique email only for active users
    op.execute("ALTER TABLE users DROP CONSTRAINT IF EXISTS users_email_key") # 1) Drop old UNIQUE(email) constraint (name is typically users_email_key)

    op.execute(
        "CREATE UNIQUE INDEX IF NOT EXISTS uq_users_email_active "
        "ON users (email) WHERE deleted_at IS NULL"
    ) # 2) Create partial unique index: only active users must have unique email

def downgrade() -> None: # Revert to UNIQUE(email) constraint
    op.execute("DROP INDEX IF EXISTS uq_users_email_active")
    op.execute("ALTER TABLE users ADD CONSTRAINT users_email_key UNIQUE (email)")