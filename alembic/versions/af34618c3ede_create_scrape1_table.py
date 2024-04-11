"""create scrape1 table

Revision ID: af34618c3ede
Revises: 
Create Date: 2024-04-11 15:45:12.593762

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'af34618c3ede'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table('scrape1',sa.Column('job_id',sa.Integer(),nullable=False,primary_key=True),
                    sa.Column('company_Names',sa.String(),nullable=False),sa.Column('job_titles',sa.String(),nullable=False),sa.Column('Location',sa.String(),nullable=False))
    pass


def downgrade():
    op.drop_table('scrape1')
    pass