"""Update fields

Revision ID: 2ef70bbd5ceb
Revises: 
Create Date: 2023-03-04 15:15:15.592140

"""
from alembic import op
import sqlalchemy as sa
from geoalchemy2 import Geometry

# revision identifiers, used by Alembic.
revision = '2ef70bbd5ceb'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=128), nullable=False),
    sa.Column('password', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('user_id')
    )
    op.create_geospatial_table('hazards',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('hazard_name', sa.String(length=128), nullable=False),
    sa.Column('category', sa.String(), nullable=True),
    sa.Column('geom', Geometry(geometry_type='POINT', spatial_index=False, from_text='ST_GeomFromEWKT', name='geometry'), nullable=True),
    sa.Column('created_by', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('modified_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['created_by'], ['users.user_id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_geospatial_index('idx_hazards_geom', 'hazards', ['geom'], unique=False, postgresql_using='gist', postgresql_ops={})
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_geospatial_index('idx_hazards_geom', table_name='hazards', postgresql_using='gist', column_name='geom')
    op.drop_geospatial_table('hazards')
    op.drop_table('users')
    # ### end Alembic commands ###