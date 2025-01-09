from datetime import datetime
from src import db

class VendorRegister(db.Model):
    __tablename__ = 'vendor_register'

    id = db.Column(db.Integer, primary_key=True)
    business_name = db.Column(db.String(100), nullable=False)
    owner_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)  # Store hashed password
    business_type = db.Column(db.String(50), nullable=False)
    mobile_number = db.Column(db.String(15), unique=True, nullable=False)
    account_no = db.Column(db.String(20), unique=True, nullable=True)  # Account number
    ifsc_code = db.Column(db.String(20), nullable=True)  # IFSC code
    aadhar_number = db.Column(db.String(15),  unique=True,nullable=True)  # Aadhar number
    pan_card_number = db.Column(db.String(10),  unique=True,nullable=True)  # Pan card number
    gst = db.Column(db.String(15), nullable=True)  # GST number
    vendor_photo = db.Column(db.String(255), nullable=True)  # Vendor photo path
    shop_photo = db.Column(db.String(255), nullable=True)  # Shop photo path
    sgo_gps_photo = db.Column(db.String(255), nullable=True)  # SGO GPS photo path
    shop_id = db.Column(db.String(10), unique=True, nullable=False)  # Unique shop ID
    status = db.Column(db.String(20), default="Active")
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())
    otp_entries = db.relationship("OTP", back_populates="user", lazy="dynamic")  # Add this line

    def __repr__(self):
        return f"<Vendor {self.business_name}>"
