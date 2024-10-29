"""date type changes in private classes

Revision ID: d8c3d44824a3
Revises: e8ff86ab2620
Create Date: 2024-10-28 23:19:48.436698

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'd8c3d44824a3'
down_revision: Union[str, None] = 'e8ff86ab2620'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('private_classes', sa.Column('start_time_unix', sa.BigInteger(), server_default='0', nullable=False))
    op.add_column('private_classes', sa.Column('duration', sa.Integer(), server_default='0', nullable=False))
    op.execute("""
                UPDATE public.private_classes
                SET start_time_unix = (EXTRACT(EPOCH FROM schedule_datetime) * 1000)::BIGINT,
                    duration = 90;
            """)
    op.drop_column('private_classes', 'assignment')
    op.drop_column('private_classes', 'schedule_datetime')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('private_classes', sa.Column('schedule_datetime', postgresql.TIMESTAMP(timezone=True), autoincrement=False, nullable=False))
    op.add_column('private_classes', sa.Column('assignment', postgresql.JSONB(astext_type=sa.Text()), autoincrement=False, nullable=True))
    op.execute("""
                UPDATE public.private_classes
                SET schedule_datetime = to_timestamp(start_time_unix / 1000);
            """)
    op.drop_column('private_classes', 'duration')
    op.drop_column('private_classes', 'start_time_unix')
    # ### end Alembic commands ###
