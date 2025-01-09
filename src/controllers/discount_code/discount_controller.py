from flask import request, jsonify
import logging
from src import db
from src.models.discount_model import Discount
from datetime import datetime

def add_discount():
    try:
        data = request.get_json()
        logging.debug(f"Received data: {data}")

        valid_from_str = data.get('valid_from')  # Assuming ISO 8601 format
        if valid_from_str:
            # Extract the date part from ISO 8601 and convert it
            valid_from = datetime.fromisoformat(valid_from_str.split("T")[0]).date()
        else:
            valid_from = None

        valid_to_str = data.get('valid_to')  # Assuming ISO 8601 format
        if valid_to_str:
            # Extract the date part from ISO 8601 and convert it
            valid_to = datetime.fromisoformat(valid_to_str.split("T")[0]).date()
        else:
            valid_to = None

        # Create a new record
        new_record = Discount(
            discount_code=data.get('discount_code'),
            discount_type=data.get('discount_type'),
            discount_value=data.get('discount_value'),
            valid_from=valid_from,
            valid_to=valid_to,
            usage_limit=data.get('usage_limit'),
            minimum_purchase_amount=data.get('minimum_purchase_amount'),
            applicable_products=data.get('applicable_products'),
            status="Active"
        )
        logging.debug(f"New record object: {new_record}")

        db.session.add(new_record)
        db.session.commit()
        return jsonify({"message": "Discount added successfully", "success": True}), 201

    except Exception as e:
        logging.error(f"Error occurred: {str(e)}")
        db.session.rollback()
        return jsonify({"message": "Error adding discount", "success": False, "msg": str(e)}), 500


def edit_discount(discount_id):
    try:
        data = request.get_json()
        logging.debug(f"Received data: {data}")

        # Retrieve the existing record from the database
        discount_record = Discount.query.get_or_404(discount_id)

        # Update the fields
        discount_record.discount_code = data.get('discount_code'),
        discount_record.discount_type = data.get('discount_type'),
        discount_record.discount_value = data.get('discount_value'),
        discount_record.valid_from = data.get('valid_from'),
        discount_record.valid_to = data.get('valid_to'),
        discount_record.usage_limit = data.get('usage_limit'),
        discount_record.minimum_purchase_amount = data.get('minimum_purchase_amount'),
        applicable_products = data.get('applicable_products', [])
        if isinstance(applicable_products, list):
            # Flatten the structure if necessary
            processed_products = [
                {"id": product["id"], "name": product["name"]}
                for product in applicable_products
                if "id" in product and "name" in product
            ]
        else:
            processed_products = []

        discount_record.applicable_products = processed_products
        
        
        discount_record.status = "Active"

        # Commit the changes to the database
        db.session.commit()

        return jsonify({"message": "Discount updated successfully", "success": True}), 200

    except Exception as e:
        logging.error(f"Error occurred: {str(e)}")
        db.session.rollback()
        return jsonify({"message": "Error updating discount", "success": False, "msg": str(e)}), 500

def delete_discount(discount_id):
    try:
        # Retrieve the existing record from the database
        record_to_delete = Discount.query.get_or_404(discount_id)

        if record_to_delete:
            # Update the status attribute
            record_to_delete.status = "Inactive"

            # Commit the changes to the database
            db.session.commit()

            return jsonify({"message": f"Discount with id {discount_id} marked as inactive successfully", "success": True}), 200
        else:
            return jsonify({"message": f"Discount with id {discount_id} not found", "success": False}), 404

    except Exception as e:
        logging.error(f"Error occurred: {str(e)}")
        db.session.rollback()
        return jsonify({"message": "Error updating discount", "success": False, "msg": str(e)}), 500

def fetch_discounts():
    try:
        email = request.args.get('email')  
        if not email:
            return jsonify({"error": "Email is required"}), 400

        records = Discount.query.filter_by(status='Active', user_id=email).all()
        
        # Create a list of dictionaries to hold the data
        data = []
        for record in records:
            data.append({
                "id": record.id,
                "discount_code": record.discount_code,
                "discount_type": record.discount_type,
                "discount_value": record.discount_value,
                "valid_from": record.valid_from,
                "valid_to": record.valid_to,
                "usage_limit": record.usage_limit,
                "minimum_purchase_amount": record.minimum_purchase_amount,
                "applicable_products": record.applicable_products
            })
        
        # Return the data as JSON
        return jsonify(data)
    except Exception as e:
        return jsonify({"message": str(e), "success": False}), 500
