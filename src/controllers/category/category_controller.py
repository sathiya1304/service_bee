from flask import request, jsonify

from src import db
import logging
from src.models.category_model import Category


    
def add_category():
    try:
        data = request.get_json()
        logging.debug(f"Received data: {data}")

        # Create a new record
        new_record = Category(
            category_name=data.get('category_name'),
            parent_category_name=data.get('parent_category_name'),
            user_id=data.get('user_id'),
            status="Active"
            )
        logging.debug(f"New record object: {new_record}")

        db.session.add(new_record)
        db.session.commit()
        return jsonify({"message": "Record added successfully", "success": True}), 201

    except Exception as e:
        logging.error(f"Error occurred: {str(e)}")
        db.session.rollback()
        return jsonify({"message": "Error adding record", "success": False, "msg": str(e)}), 500

def edit_category(category_id):
    try:
        data = request.get_json()
        logging.debug(f"Received data: {data}")

        # Retrieve the existing record from the database
        category_record = Category.query.get_or_404(category_id)

        # Update the category_name attribute
        category_record.category_name = data.get('category_name'),
        category_record.parent_category_name = data.get('parent_category_name'),
        category_record.status = "Active"

        # Commit the changes to the database
        db.session.commit()

        return jsonify({"message": "Record updated successfully", "success": True}), 200

    except Exception as e:
        logging.error(f"Error occurred: {str(e)}")
        db.session.rollback()
        return jsonify({"message": "Error updating record", "success": False, "msg": str(e)}), 500


def delete_category(category_id):
    try:
        # Retrieve the existing record from the database
        record_to_delete = Category.query.get_or_404(category_id)

        if record_to_delete:
            # Update the status attribute
            record_to_delete.status = "InActive"

            # Commit the changes to the database
            db.session.commit()

            return jsonify({"message": f"Record with id {category_id} marked as inactive successfully", "success": True}), 200
        else:
            return jsonify({"message": f"Record with id {category_id} not found", "success": False}), 404

    except Exception as e:
        logging.error(f"Error occurred: {str(e)}")
        db.session.rollback()
        return jsonify({"message": "Error updating record", "success": False, "msg": str(e)}), 500


def fetch_category():
    try:
        email = request.args.get('email')  
        if not email:
            return jsonify({"error": "Email is required"}), 400

        print(f"Email received: {email}") 
        records = Category.query.filter_by(status='Active', user_id=email).all()

        data = []
        for record in records:
            data.append({
                "id": record.id,
                "category_name": record.category_name,
                "parent_category_name": record.parent_category_name,
            })

        # Return the data as JSON
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
