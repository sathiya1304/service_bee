
from src import db

class Discount(db.Model):
    __tablename__ = 'discount'

    id = db.Column(db.Integer, primary_key=True)
    discount_code = db.Column(db.String(100), nullable=False, unique=True)  # Unique discount code
    discount_type = db.Column(db.String(50), nullable=False)  # Type of discount (e.g., percentage, flat)
    discount_value = db.Column(db.Float, nullable=False)  # Discount value (e.g., 67.45 or 50)
    valid_from = db.Column(db.Date, nullable=False)  # Start date for the discount
    valid_to = db.Column(db.Date, nullable=False)  # End date for the discount
    usage_limit = db.Column(db.Float, nullable=True)  # Limit on usage (can be float)
    minimum_purchase_amount = db.Column(db.Float, nullable=True)  # Minimum purchase amount
    applicable_products = db.Column(db.JSON, nullable=True)  # JSONB field for PostgreSQL
    status = db.Column(db.String(20), default="Active")  # Status of the discount
    created_at = db.Column(db.DateTime, default=db.func.now())  # Timestamp for creation
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())  # Timestamp for updates


