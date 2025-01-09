from flask import request, jsonify
from src import db
import logging
from src.models.order_details_model import OrderDetails
from src.models.products_model import ProductDetail

from sqlalchemy import func
from flask import jsonify
import logging

from sqlalchemy import func
import logging
from flask import jsonify
from datetime import datetime

def fetch_counts():
    try:
        # Query the database for counts
        sales_count = OrderDetails.query.filter_by(order_status='delivered').count()
        pending_count=OrderDetails.query.filter_by(order_status='pending').count()
        reject_count=OrderDetails.query.filter_by(order_status='reject').count()
        product_count = ProductDetail.query.count()
        customer_count = db.session.query(OrderDetails.customer_name).distinct().count()
        order_count = OrderDetails.query.count()

        # Aggregate daily order counts by day of the week (1: Sunday, 2: Monday, ..., 7: Saturday)
        daily_orders = db.session.query(
            func.dayofweek(OrderDetails.order_date).label("day_of_week"),
            func.count(OrderDetails.id).label("order_count")
        ).group_by(func.dayofweek(OrderDetails.order_date)).all()

        # Map day_of_week (1-7) to the actual name of the day
        days_of_week = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]

        # Initialize a dictionary with 0 order count for each day
        daily_order_data = {day: 0 for day in days_of_week}

        # Update the daily order data with actual order counts from the database
        for row in daily_orders:
            day_name = days_of_week[int(row.day_of_week) - 1]  # Adjusting to 0-based index
            daily_order_data[day_name] = row.order_count

        # Convert dictionary to list for frontend compatibility
        daily_order_data = [{"day": day, "count": count} for day, count in daily_order_data.items()]

        # Aggregate monthly order counts for the current and previous month
        current_month = datetime.now().month
        previous_month = current_month - 1 if current_month > 1 else 12
        current_year = datetime.now().year
        
        monthly_orders = db.session.query(
            func.month(OrderDetails.order_date).label("month"),
            func.count(OrderDetails.id).label("order_count")
        ).filter(
            func.extract('year', OrderDetails.order_date) == current_year
        ).group_by(func.month(OrderDetails.order_date)).all()

        # Get monthly order counts for current and previous month (ensure both months are included in the response)
        monthly_order_data = {month: 0 for month in [previous_month, current_month]}
        for row in monthly_orders:
            monthly_order_data[row.month] = row.order_count
        
        # Convert monthly data to a list for frontend compatibility
        monthly_order_data = [{"month": month, "count": count} for month, count in monthly_order_data.items()]

        # Return counts and both daily and monthly order data as JSON
        return jsonify({
            "sales_count": sales_count,
            "product_count": product_count,
            "customer_count": customer_count,
            "order_count": order_count,
            "daily_orders": daily_order_data,
            "monthly_orders": monthly_order_data,
            "pending_count":pending_count,
            "reject_count":reject_count
        }), 200

    except Exception as e:
        # Log the error with full stack trace for better debugging
        logging.error(f"Error fetching counts: {str(e)}")
        logging.debug(f"Exception details: {e}", exc_info=True)  # Logs detailed traceback
        return jsonify({"error": f"An error occurred while fetching the counts: {str(e)}"}), 500



        
        

