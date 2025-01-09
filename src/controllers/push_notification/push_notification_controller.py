from flask import request, jsonify
import logging
from src import db
from src.models.push_notification_model import PushNotification
from datetime import datetime



def add_push_notification():
    try:
        data = request.get_json()
        logging.debug(f"Received data: {data}")
        

        schedule_date_str = data.get('schedule_date')  # Assuming ISO 8601 format
        if schedule_date_str:
            # Extract the date part from ISO 8601 and convert it
            schedule_date = datetime.fromisoformat(schedule_date_str.split("T")[0]).date()
        else:
            schedule_date = None


        schedule_time_str = data.get('schedule_time')
        if schedule_time_str:
            schedule_time = datetime.strptime(schedule_time_str, "%H:%M:%S").time()
        else:
            schedule_time = None

        # Create a new record
        new_notification = PushNotification(
            title=data.get('title'),
            message=data.get('message'),
            schedule_date=schedule_date,
            schedule_time=schedule_time,
            status="Active"
        )
        logging.debug(f"New notification object: {new_notification}")

        db.session.add(new_notification)
        db.session.commit()
        return jsonify({"message": "Push notification added successfully", "success": True}), 201

    except Exception as e:
        logging.error(f"Error occurred: {str(e)}")
        db.session.rollback()
        return jsonify({"message": "Error adding push notification", "success": False, "msg": str(e)}), 500

def edit_push_notification(notification_id):
    try:
        data = request.get_json()
        logging.debug(f"Received data: {data}")

        schedule_time_str = data.get('schedule_time')
        if schedule_time_str:
            schedule_time = datetime.strptime(schedule_time_str, "%H:%M:%S").time()
        else:
            schedule_time = None
        
        # Retrieve the existing record from the database
        notification_record = PushNotification.query.get_or_404(notification_id)

        # Update the fields
        notification_record.title = data.get('title')
        notification_record.message = data.get('message')
        notification_record.schedule_date = data.get('schedule_date')
        notification_record.schedule_time = schedule_time
        notification_record.status = data.get('status', notification_record.status)

        # Commit the changes to the database
        db.session.commit()

        return jsonify({"message": "Push notification updated successfully", "success": True}), 200

    except Exception as e:
        logging.error(f"Error occurred: {str(e)}")
        db.session.rollback()
        return jsonify({"message": "Error updating push notification", "success": False, "msg": str(e)}), 500

def delete_push_notification(notification_id):
    try:
        # Retrieve the existing record from the database
        record_to_delete = PushNotification.query.get_or_404(notification_id)

        if record_to_delete:
            # Update the status attribute
            record_to_delete.status = "Inactive"

            # Commit the changes to the database
            db.session.commit()

            return jsonify({"message": f"Push notification with id {notification_id} marked as inactive successfully", "success": True}), 200
        else:
            return jsonify({"message": f"Push notification with id {notification_id} not found", "success": False}), 404

    except Exception as e:
        logging.error(f"Error occurred: {str(e)}")
        db.session.rollback()
        return jsonify({"message": "Error updating push notification", "success": False, "msg": str(e)}), 500
    

def fetch_push_notifications():
    try:
        email = request.args.get('email')  
        if not email:
            return jsonify({"error": "Email is required"}), 400
        records = PushNotification.query.filter_by(status='Active', user_id=email).all()
        
        # Create a list of dictionaries to hold the data
        data = []
        for record in records:
            data.append({
                "notification_id": record.notification_id,
                "title": record.title,
                "message": record.message,
                "schedule_date": record.schedule_date,
                "schedule_time": record.schedule_time.strftime("%H:%M:%S") if record.schedule_time else "",  # Convert time object to string
                "status": record.status
            })
        
        # Return the data as JSON
        return jsonify(data)
    except Exception as e:
        logging.error(f"Error occurred: {str(e)}")
        return jsonify({"message": str(e), "success": False}), 500    
    
