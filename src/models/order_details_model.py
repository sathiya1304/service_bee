from src import db

class OrderDetails(db.Model):
    __tablename__ = 'order_deatils'

    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(100), nullable=False)
    order_date = db.Column(db.Date, nullable=False)
    shipping_address = db.Column(db.String(100), nullable=False)
    billing_address = db.Column(db.String(100), nullable=False)
    order_items = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.String(100), nullable=False)
    price = db.Column(db.String(100), nullable=False)
    total_amount = db.Column(db.String(100), nullable=False)
    payment_status = db.Column(db.String(100), nullable=False)
    order_status = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(20), default="Active")
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())