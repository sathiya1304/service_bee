from flask import jsonify, request
from flask_mail import Message
import random
import string
from datetime import datetime, timedelta
from src import db, mail
from src.models.vendor_register_model import VendorRegister
from src.models.otp_model import OTP

def generate_otp_controller():
    try:
        # Get email and password from request
        data = request.get_json()
        email_id = data.get("email_id")
        password = data.get("password")

        if not email_id or not password:
            return jsonify({"message": "Both email_id and password are required", "status": 0}), 400

        # Check if user exists with the provided email
        user = VendorRegister.query.filter_by(email=email_id).first()

        if not user:
            return jsonify({"message": "Email not found in VendorRegister", "status": 0}), 404

        # Verify the password matches the email
        if user.password != password:  # Plain text password comparison
            return jsonify({"message": "Password is incorrect", "status": 0}), 401

        # Generate a 6-digit OTP
        otp = ''.join(random.choices(string.digits, k=6))
        otp_expiry_time = datetime.now() + timedelta(minutes=5)  # OTP valid for 5 minutes

        # Save OTP to the database
        otp_entry = OTP(user_id=user.id, otp=otp, expiry_time=otp_expiry_time)
        db.session.add(otp_entry)
        db.session.commit()

        # Send OTP via email
        msg = Message(
            subject="Your OTP Code",
            recipients=[email_id],
            body=f"Your 6-digit OTP code is {otp}. It will expire in 5 minutes."
        )
        mail.send(msg)

        return jsonify({"message": "OTP sent successfully to your email", "status": 1}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Error: {str(e)}", "status": 0}), 500




def validate_otp_controller():
    try:
        # Get email and OTP from request
        data = request.get_json()
        email_id = data.get("email_id")
        otp = data.get("otp")

        if not email_id or not otp:
            return jsonify({"message": "email_id and otp are required", "status": 0}), 400

        # Check if user exists with the provided email
        user = VendorRegister.query.filter_by(email=email_id).first()

        if not user:
            return jsonify({"message": "Email not found", "status": 0}), 404

        # Check if OTP exists for the user
        otp_entry = OTP.query.filter_by(user_id=user.id, otp=otp).first()

        if not otp_entry:
            return jsonify({"message": "Invalid OTP", "status": 0}), 400

        # Check if OTP has expired
        if otp_entry.expiry_time < datetime.now():
            return jsonify({"message": "OTP has expired", "status": 0}), 400

        # OTP is valid, proceed to dashboard or return success
        return jsonify({"message": "OTP validated successfully", "status": 1, "redirect": "/dashboard"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Error: {str(e)}", "status": 0}), 500
