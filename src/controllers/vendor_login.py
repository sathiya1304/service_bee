from datetime import timedelta
from flask import jsonify, request
from src import db
from src.models.vendor_register_model import VendorRegister
from sqlalchemy.exc import OperationalError
from flask_jwt_extended import create_access_token

def vendor_login_controller():
    try:
        data = request.get_json()
        email_id = data.get("email_id")
        password = data.get("password")

        if not email_id or not password:
            return jsonify({"message": "email_id and password are required", "status": 0}), 400

        # Check if a user exists with the specified email_id
        user = VendorRegister.query.filter_by(email=email_id).first()

        if not user:
            return jsonify({"message": "Invalid email_id", "status": 0, "error_type": "wrong_email"}), 401
        
        # Check if the password matches
        if user.password != password:
            return jsonify({"message": "Invalid password", "status": 0, "error_type": "wrong_password"}), 401

        # If both email_id and password are valid
        additional_claims = {
            "user_id": user.id,
            "email_id": user.email,
        }

        access_token = create_access_token(
            identity=user.id,
            additional_claims=additional_claims,
            expires_delta=timedelta(days=1)
        )
        return jsonify(
            {
                "message": "Login successful",
                "token": access_token,
                "email_id": user.email,
                "status": 1,
            }
        ), 200

    except OperationalError as e:
        db.session.rollback()
        if "MySQL server has gone away" in str(e):
            return jsonify({"message": "Database connection lost. Please try again later.", "status": 0}), 500
        else:
            return jsonify({"success": 0, "error": str(e)}), 500

    except Exception as e:
        db.session.rollback()
        return jsonify({"success": 0, "error": str(e)}), 500


