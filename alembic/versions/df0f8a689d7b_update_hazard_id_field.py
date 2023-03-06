"""Update hazard id field

Revision ID: df0f8a689d7b
Revises: 2ef70bbd5ceb
Create Date: 2023-03-04 16:31:14.762649

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'df0f8a689d7b'
down_revision = '2ef70bbd5ceb'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('hazards', 'created_by',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('hazards', 'created_by',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###
