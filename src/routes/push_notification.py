from flask import Blueprint
from src.controllers.push_notification.push_notification_controller import (
    add_push_notification,
    edit_push_notification,
    delete_push_notification,
    fetch_push_notifications,
)

push_notification_bp = Blueprint('push_notification', __name__, url_prefix='/push_notification')

# Add Push Notification
@push_notification_bp.route('/add', methods=['POST'])
def add_push_notification_controller():
    return add_push_notification()

# Edit Push Notification
@push_notification_bp.route('/edit/<int:notification_id>', methods=['PUT'])
def edit_push_notification_controller(notification_id):
    return edit_push_notification(notification_id)

# Delete Push Notification
@push_notification_bp.route('/delete/<int:notification_id>', methods=['DELETE'])
def delete_push_notification_controller(notification_id):
    return delete_push_notification(notification_id)

# Fetch Push Notifications
@push_notification_bp.route('/fetch', methods=['GET'])
def fetch_push_notifications_controller():
    return fetch_push_notifications()
