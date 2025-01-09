from datetime import datetime
from src import db

class OTP(db.Model):
    __tablename__ = 'otp'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('vendor_register.id'), nullable=False)
    otp = db.Column(db.String(6), nullable=False)
    expiry_time = db.Column(db.DateTime, nullable=False)

    user = db.relationship("VendorRegister", back_populates="otp_entries")  # This is the back relationship

    def __repr__(self):
        return f"<OTP {self.otp}>"
