import os
from flask import Blueprint, jsonify, request
from src.controllers.discount_code.discount_controller  import add_discount,edit_discount,delete_discount,fetch_discounts

discount_bp = Blueprint('discount', __name__, url_prefix='/discount')

# Add Discount
@discount_bp.route('/add', methods=['POST'])
def add_discount_controller():
    return add_discount()

# Edit Discount
@discount_bp.route('/edit/<int:discount_id>', methods=['PUT'])
def edit_discount_controller(discount_id):
    return edit_discount(discount_id)

# Delete Discount
@discount_bp.route('/delete/<int:discount_id>', methods=['DELETE'])
def delete_discount_controller(discount_id):
    return delete_discount(discount_id)

# Fetch Discounts
@discount_bp.route('/fetch', methods=['GET'])
def fetch_discounts_controller():
    return fetch_discounts()
