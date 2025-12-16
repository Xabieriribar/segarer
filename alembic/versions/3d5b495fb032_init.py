"""init

Revision ID: 3d5b495fb032
Revises: 802f5039000b
Create Date: 2025-12-16 11:41:18.964403

"""
from typing import Sequence, Union



# revision identifiers, used by Alembic.
revision: str = '3d5b495fb032'
down_revision: Union[str, Sequence[str], None] = '802f5039000b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
