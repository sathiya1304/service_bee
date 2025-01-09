from flask import Blueprint, request, jsonify
from src import db
from src.models.vendor_register_model import VendorRegister
import logging
import re
from werkzeug.utils import secure_filename
import os




def generate_unique_shop_id(shop_name):
    # Extract the first 3 letters of the shop name
    prefix = re.sub(r'[^A-Za-z]', '', shop_name)[:3].upper()  # Only take the first 3 letters (alphabets only)
    existing_vendor = VendorRegister.query.filter(
        VendorRegister.shop_id.like(f"{prefix}%")
    ).order_by(db.desc(VendorRegister.shop_id)).first()

    if existing_vendor:
        last_number = int(existing_vendor.shop_id[-3:]) + 1  # Get the last numeric part and increment
    else:
        last_number = 1  # If no existing vendor, start with 001

    return f"{prefix}{last_number:03d}"

def add_vendor_register():
    try:
        data = request.get_json()
        logging.debug(f"Received data: {data}")

        # Check if a record with the same email or mobile number already exists
        existing_vendor = VendorRegister.query.filter(
            (VendorRegister.email == data.get('email')) |
            (VendorRegister.mobile_number == data.get('mobile_number'))
        ).first()

        if existing_vendor:
            logging.warning("Vendor with the same email or mobile number already exists.")
            return jsonify({"message": "A vendor with this email or mobile number already exists.", "success": False}), 409

        # Generate unique shop ID
        shop_id = generate_unique_shop_id(data.get('business_name'))

        # Create a new vendor record
        new_vendor = VendorRegister(
            business_name=data.get('business_name'),
            owner_name=data.get('owner_name'),
            email=data.get('email'),
            password=data.get('password'),  # Ensure this is hashed for security
            business_type=data.get('business_type'),
            mobile_number=data.get('mobile_number'),
            status="Active",
            shop_id=shop_id  # Add the generated unique shop ID
        )
        logging.debug(f"New vendor record: {new_vendor}")

        db.session.add(new_vendor)
        db.session.commit()

        return jsonify({"message": "Vendor registered successfully", "success": True, "shop_id": shop_id}), 201

    except Exception as e:
        logging.error(f"Error occurred: {str(e)}")
        db.session.rollback()
        return jsonify({"message": "Error registering vendor", "success": False, "msg": str(e)}), 500
    

def update_vendor_bank_details():
    try:
        data = request.get_json()
        logging.debug(f"Received data for update: {data}")
        print(f"Received data: {data}")

        # Validate required fields
        required_fields = ["email", "mobile_number", "account_number", "ifsc_code", "account_holder_name", "aadhar_number", "pan_card_number"]
        missing_fields = [field for field in required_fields if not data.get(field)]
        if missing_fields:
            logging.warning(f"Missing fields: {missing_fields}")
            return jsonify({"message": f"Missing fields: {', '.join(missing_fields)}", "success": False}), 400

      # Check for duplicate account number
        if VendorRegister.query.filter(
            VendorRegister.account_no == data.get("account_number"),
            VendorRegister.email != data.get("email")  # Exclude the current vendor
        ).first():
            return jsonify({"message": "Account number is already in use by another vendor.", "success": False}), 409

        # Check for duplicate IFSC code and account combination
        if VendorRegister.query.filter(
            VendorRegister.account_no == data.get("account_number"),
            VendorRegister.ifsc_code == data.get("ifsc_code"),
            VendorRegister.email != data.get("email")  # Exclude the current vendor
        ).first():
            return jsonify({"message": "Account number with this IFSC code is already in use.", "success": False}), 409

        # Check for duplicate PAN card number
        if VendorRegister.query.filter(
            VendorRegister.pan_card_number == data.get("pan_card_number"),
            VendorRegister.email != data.get("email")  # Exclude the current vendor
        ).first():
            return jsonify({"message": "PAN card number is already in use by another vendor.", "success": False}), 409

        # Check for duplicate Aadhar card number
        if VendorRegister.query.filter(
            VendorRegister.aadhar_number == data.get("aadhar_number"),
            VendorRegister.email != data.get("email")  # Exclude the current vendor
        ).first():
            return jsonify({"message": "Aadhar card number is already in use by another vendor.", "success": False}), 409
        # Find the vendor by email or mobile number (email is preferred)
        vendor = VendorRegister.query.filter(
            (VendorRegister.email.ilike(data.get("email"))) |
            (VendorRegister.mobile_number == data.get("mobile_number"))
        ).first()

        if not vendor:
            logging.warning("Vendor not found.")
            return jsonify({"message": "Vendor not found", "success": False}), 404

        # Extract the shop_id (this was generated during the first step and is stored in the vendor record)
        shop_id = vendor.shop_id

        # Update vendor bank details
        vendor.account_no = data.get("account_number")
        vendor.ifsc_code = data.get("ifsc_code")
        vendor.account_holder_name = data.get("account_holder_name")
        vendor.aadhar_number = data.get("aadhar_number")
        vendor.pan_card_number = data.get("pan_card_number")
        vendor.gst = data.get("gst_number")  # Optional field

        db.session.commit()

        logging.info(f"Vendor bank details updated successfully for shop_id: {shop_id}.")
        return jsonify({"message": "Vendor bank details updated successfully", "success": True, "shop_id": shop_id}), 200

    except Exception as e:
        logging.error(f"Error occurred during update: {str(e)}")
        db.session.rollback()
        return jsonify({"message": "Error updating vendor bank details", "success": False, "msg": str(e)}), 500
    
    # Configure the base upload folder and the subdirectory for vendor images

BASE_UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
VENDOR_IMAGE_FOLDER = os.path.join(BASE_UPLOAD_FOLDER, 'vendor_images')

# Ensure the vendor_images directory exists
os.makedirs(VENDOR_IMAGE_FOLDER, exist_ok=True)

# Function to check if the file extension is allowed
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Update Vendor Images

def update_vendor_images():
    try:
        data = request.form  # Get form data
        # Find the vendor by email or mobile number (email is preferred)
        vendor = VendorRegister.query.filter(
            (VendorRegister.email == data.get("email")) |
            (VendorRegister.mobile_number == data.get("mobile_number"))
        ).first()

        if not vendor:
            return jsonify({"message": "Vendor not found", "success": False}), 404

        # Initialize response dictionary
        updated_fields = {}

        # Check for file uploads and save them in the vendor_images folder
        if 'vendor_photo' in request.files:
            vendor_photo = request.files['vendor_photo']
            if vendor_photo and allowed_file(vendor_photo.filename):
                filename = secure_filename(f"vendor_{vendor.id}_photo_{vendor_photo.filename}")
                filepath = os.path.join(VENDOR_IMAGE_FOLDER, filename)
                vendor_photo.save(filepath)
                vendor.vendor_photo = os.path.join('vendor_images', filename)  # Store relative path
                updated_fields['vendor_photo'] = vendor.vendor_photo

        if 'shop_photo' in request.files:
            shop_photo = request.files['shop_photo']
            if shop_photo and allowed_file(shop_photo.filename):
                filename = secure_filename(f"vendor_{vendor.id}_shop_{shop_photo.filename}")
                filepath = os.path.join(VENDOR_IMAGE_FOLDER, filename)
                shop_photo.save(filepath)
                vendor.shop_photo = os.path.join('vendor_images', filename)  # Store relative path
                updated_fields['shop_photo'] = vendor.shop_photo

        if 'gps_photo' in request.files:
            gps_photo = request.files['gps_photo']
            if gps_photo and allowed_file(gps_photo.filename):
                filename = secure_filename(f"vendor_{vendor.id}_gps_{gps_photo.filename}")
                filepath = os.path.join(VENDOR_IMAGE_FOLDER, filename)
                gps_photo.save(filepath)
                vendor.sgo_gps_photo = os.path.join('vendor_images', filename)  # Store relative path
                updated_fields['gps_photo'] = vendor.sgo_gps_photo

        # Commit the changes to the database
        db.session.commit()

        # Return a success response
        return jsonify({
            "message": "Vendor photos updated successfully",
            "success": True,
            "updated_fields": updated_fields
        }), 200

    except Exception as e:
        db.session.rollback()
        logging.error(f"Error updating vendor photos: {str(e)}")
        return jsonify({
            "message": f"Error updating vendor photos: {str(e)}",
            "success": False
        }), 500


def update_vendor_basic_details():
    try:
        data = request.get_json()
        logging.debug(f"Received data for basic details update: {data}")

        # Validate required fields
        required_fields = ["email", "business_name", "owner_name", "mobile_number", "business_type"]
        missing_fields = [field for field in required_fields if not data.get(field)]
        if missing_fields:
            logging.warning(f"Missing fields: {missing_fields}")
            return jsonify({"message": f"Missing fields: {', '.join(missing_fields)}", "success": False}), 400

        # Find the vendor by email or mobile number (email is preferred)
        vendor = VendorRegister.query.filter(
            (VendorRegister.email.ilike(data.get("email"))) |
            (VendorRegister.mobile_number == data.get("mobile_number"))
        ).first()

        if not vendor:
            logging.warning("Vendor not found.")
            return jsonify({"message": "Vendor not found", "success": False}), 404

        # Check for duplicate email or mobile number
        if VendorRegister.query.filter(
            (VendorRegister.email == data.get("email")) & (VendorRegister.id != vendor.id)
        ).first():
            return jsonify({"message": "Email is already in use by another vendor.", "success": False}), 409

        if VendorRegister.query.filter(
            (VendorRegister.mobile_number == data.get("mobile_number")) & (VendorRegister.id != vendor.id)
        ).first():
            return jsonify({"message": "Mobile number is already in use by another vendor.", "success": False}), 409

        # Update vendor basic details
        vendor.business_name = data.get("business_name")
        vendor.owner_name = data.get("owner_name")
        vendor.mobile_number = data.get("mobile_number")
        vendor.email = data.get("email")
        vendor.business_type = data.get("business_type")

        # Update password only if provided
        if data.get("password"):
            vendor.password = data.get("password")  # Ensure hashing if applicable

        db.session.commit()

        logging.info(f"Vendor basic details updated successfully for vendor ID: {vendor.id}")
        return jsonify({"message": "Vendor basic details updated successfully", "success": True}), 200

    except Exception as e:
        logging.error(f"Error occurred while updating vendor basic details: {str(e)}")
        db.session.rollback()
        return jsonify({"message": "Error updating vendor details", "success": False, "msg": str(e)}), 500

