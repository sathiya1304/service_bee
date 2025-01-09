from src import db

class Category(db.Model):
    __tablename__ = 'category'

    id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(100), nullable=False)
    parent_category_name = db.Column(db.String(100), nullable=False)
    parent_category_id = db.Column(db.String(100), nullable=True)
    user_id = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(20), default="Active")
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())