import os
from flask import Blueprint
from flask import Flask, jsonify, send_from_directory
from src.controllers.category.category_controller import add_category,edit_category,delete_category,fetch_category
category_bp = Blueprint('category', __name__, url_prefix='/category')

#vendorLogin
@category_bp.route('/add', methods=['POST'])
def add_category_controller():
    return add_category()


@category_bp.route('/edit/<int:category_id>', methods=['PUT'])
def edit_category_controller(category_id):
    return edit_category(category_id)


@category_bp.route('/delete/<int:category_id>', methods=['DELETE'])
def delete_category_controller(category_id):
    return delete_category(category_id)

@category_bp.route('/fetch')
def category_fetch_controller():
    return fetch_category()

