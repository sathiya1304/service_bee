from src import db

class ProductDetail(db.Model):
    __tablename__ = 'product_details'

    product_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    price = db.Column(db.Float)
    discount_price = db.Column(db.Float, nullable=True)
    sku = db.Column(db.String(100))
    stock_quantity = db.Column(db.Integer)
    product_images = db.Column(db.JSON)  # To store JSON array of image names
    product_videos=db.Column(db.JSON)
    vendor_id = db.Column(db.Integer, db.ForeignKey('vendor_register.id'))
    status = db.Column(db.String(50), default='Active')
