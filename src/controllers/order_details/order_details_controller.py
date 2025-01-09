from flask import request, jsonify
from src import db
import logging
from src.models.order_details_model import OrderDetails


def delete_order_details(order_details_id):
    try:
        # Retrieve the existing record from the database
        record_to_delete = OrderDetails.query.get_or_404(order_details_id)

        if record_to_delete:
            # Update the status attribute
            record_to_delete.order_status = "reject"

            # Commit the changes to the database
            db.session.commit()

            return jsonify({"message": f"Record with id {order_details_id} marked as inactive successfully", "success": True}), 200
        else:
            return jsonify({"message": f"Record with id {order_details_id} not found", "success": False}), 404

    except Exception as e:
        logging.error(f"Error occurred: {str(e)}")
        db.session.rollback()
        return jsonify({"message": "Error updating record", "success": False, "msg": str(e)}), 500


def fetch_order_details():
    try:
        email = request.args.get('email')  
        if not email:
            return jsonify({"error": "Email is required"}), 400
        records = OrderDetails.query.filter_by(status='Active', user_id=email).all()
        
        # Create a list of dictionaries to hold the data
        data = []
        for record in records:
            data.append({
                "id": record.id,
                "customer_name": record.customer_name,
                "order_date": record.order_date,
                "shipping_address": record.shipping_address,
                "billing_address": record.billing_address,
                "order_items": record.order_items,
                "quantity": record.quantity,
                "price": record.price,
                "total_amount": record.total_amount,
                "payment_status": record.payment_status,
                "order_status": record.order_status,
            })
        
        # Return the data as JSON
        return jsonify(data)
    except Exception as e:
        return jsonify({data: str(e)}), 500
