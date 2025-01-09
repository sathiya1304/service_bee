import os
from flask import Blueprint
from flask import Flask, jsonify, send_from_directory
from src.controllers.order_details.order_details_controller import delete_order_details,fetch_order_details
order_details_bp = Blueprint('order_details', __name__, url_prefix='/order_details')



@order_details_bp.route('/delete/<int:order_details_id>', methods=['DELETE'])
def delete_order_details_controller(order_details_id):
    return delete_order_details(order_details_id)

@order_details_bp.route('/fetch')
def order_details_fetch_controller():
    return fetch_order_details()

