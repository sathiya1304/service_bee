"""Initial migration

Revision ID: d8e06eddc49c
Revises: 1a8ccc98d66c
Create Date: 2025-01-08 12:16:18.872808

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd8e06eddc49c'
down_revision = '1a8ccc98d66c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('otp', schema=None) as batch_op:
        batch_op.create_foreign_key(None, 'vendor_register', ['user_id'], ['id'])

    with op.batch_alter_table('product_details', schema=None) as batch_op:
        batch_op.create_foreign_key(None, 'category', ['category_id'], ['id'])
        batch_op.create_foreign_key(None, 'vendor_register', ['vendor_id'], ['id'])

    with op.batch_alter_table('vendor_register', schema=None) as batch_op:
        batch_op.add_column(sa.Column('account_no', sa.String(length=20), nullable=True))
        batch_op.add_column(sa.Column('ifsc_code', sa.String(length=20), nullable=True))
        batch_op.add_column(sa.Column('aadhar_number', sa.String(length=15), nullable=True))
        batch_op.add_column(sa.Column('pan_card_number', sa.String(length=10), nullable=True))
        batch_op.add_column(sa.Column('gst', sa.String(length=15), nullable=True))
        batch_op.add_column(sa.Column('vendor_photo', sa.String(length=255), nullable=True))
        batch_op.add_column(sa.Column('shop_photo', sa.String(length=255), nullable=True))
        batch_op.add_column(sa.Column('sgo_gps_photo', sa.String(length=255), nullable=True))
        batch_op.add_column(sa.Column('shop_id', sa.String(length=10), nullable=False))
        batch_op.create_unique_constraint(None, ['shop_id'])
        batch_op.create_unique_constraint(None, ['aadhar_number'])
        batch_op.create_unique_constraint(None, ['account_no'])
        batch_op.create_unique_constraint(None, ['pan_card_number'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('vendor_register', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')
        batch_op.drop_constraint(None, type_='unique')
        batch_op.drop_constraint(None, type_='unique')
        batch_op.drop_constraint(None, type_='unique')
        batch_op.drop_column('shop_id')
        batch_op.drop_column('sgo_gps_photo')
        batch_op.drop_column('shop_photo')
        batch_op.drop_column('vendor_photo')
        batch_op.drop_column('gst')
        batch_op.drop_column('pan_card_number')
        batch_op.drop_column('aadhar_number')
        batch_op.drop_column('ifsc_code')
        batch_op.drop_column('account_no')

    with op.batch_alter_table('product_details', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')

    with op.batch_alter_table('otp', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')

    # ### end Alembic commands ###
