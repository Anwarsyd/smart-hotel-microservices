"""add email verification fields

Revision ID: 6e3c95c988d2
Revises: 29754f57d7e4
Create Date: 2025-09-30 17:23:43.135783

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from datetime import datetime


# revision identifiers, used by Alembic.
revision: str = '6e3c95c988d2'
down_revision: Union[str, Sequence[str], None] = '29754f57d7e4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Add verification_token_expires (nullable)
    op.add_column('users', sa.Column('verification_token_expires', sa.DateTime(), nullable=True))
    
    # Add timestamp columns as nullable first
    op.add_column('users', sa.Column('created_at', sa.DateTime(), nullable=True))
    op.add_column('users', sa.Column('updated_at', sa.DateTime(), nullable=True))
    
    # Update existing rows with current timestamp
    op.execute(f"UPDATE users SET created_at = '{datetime.utcnow()}' WHERE created_at IS NULL")
    op.execute(f"UPDATE users SET updated_at = '{datetime.utcnow()}' WHERE updated_at IS NULL")
    
    # Now make them NOT NULL
    op.alter_column('users', 'created_at', nullable=False)
    op.alter_column('users', 'updated_at', nullable=False)
    
    # Make is_verified NOT NULL (set default False for existing users)
    op.execute("UPDATE users SET is_verified = FALSE WHERE is_verified IS NULL")
    op.alter_column('users', 'is_verified', existing_type=sa.BOOLEAN(), nullable=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column('users', 'is_verified', existing_type=sa.BOOLEAN(), nullable=True)
    op.drop_column('users', 'updated_at')
    op.drop_column('users', 'created_at')
    op.drop_column('users', 'verification_token_expires')