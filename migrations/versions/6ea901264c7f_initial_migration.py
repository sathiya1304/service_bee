"""Initial migration

Revision ID: 6ea901264c7f
Revises: 360b04c1d433
Create Date: 2025-01-08 12:00:21.595978

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6ea901264c7f'
down_revision = '360b04c1d433'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('otp', schema=None) as batch_op:
        batch_op.create_foreign_key(None, 'vendor_register', ['user_id'], ['id'])

    with op.batch_alter_table('product_details', schema=None) as batch_op:
        batch_op.create_foreign_key(None, 'vendor_register', ['vendor_id'], ['id'])
        batch_op.create_foreign_key(None, 'category', ['category_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('product_details', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')

    with op.batch_alter_table('otp', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')

    # ### end Alembic commands ###
