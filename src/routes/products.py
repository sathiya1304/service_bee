from flask import Blueprint
from src.controllers.products.products_controller import add_product, edit_product, delete_product, fetch_product

product_bp = Blueprint('product', __name__, url_prefix='/product')

@product_bp.route('/add', methods=['POST'])
def add_product_controller():
    return add_product()

@product_bp.route('/edit/<int:product_id>', methods=['PUT'])
def edit_product_controller(product_id):
    return edit_product(product_id)

@product_bp.route('/delete/<int:product_id>', methods=['DELETE'])
def delete_product_controller(product_id):
    return delete_product(product_id)

@product_bp.route('/fetch')
def fetch_product_controller():
    return fetch_product()
